# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""X-Accel-Redirect support for InvenioRDM file downloads.

Monkeypatches ``Transfer.send_file`` from invenio-records-resources so that
local files are handed off to nginx instead of being streamed by uWSGI.
The permission checks still run in InvenioRDM before ``send_file`` is called;
only the way the bytes are delivered changes.
"""

import json
import posixpath
import unicodedata
from urllib.parse import quote, urlsplit

from flask import current_app, make_response
from werkzeug.exceptions import InternalServerError

#: Storage root on disk -> nginx internal location prefix.
#: Override per environment with ``XSENDFILE_PREFIX_MAP`` in invenio.cfg.
DEFAULT_PREFIX_MAP = {
    "/mnt/content": "/mnt/content/",
    "/mnt/content1": "/mnt/u/content1/",
    "/mnt/test_dir": "/mnt/test_dir/",
}

#: If the X-Accel response can't be built, files up to this size are still
#: streamed by uWSGI. Larger files fail with a 500 instead, so a
#: misconfiguration can't silently bring back worker exhaustion.
#: Override with ``XSENDFILE_FALLBACK_MAX_SIZE`` in invenio.cfg.
DEFAULT_FALLBACK_MAX_SIZE = 100 * 1024 * 1024  # 100 MiB

# Based on invenio-files-rest (helpers.sanitize_mimetype / send_stream), which
# the original streaming path applies, plus PDF and video so they can be
# previewed and opened in the browser. These open in the browser's built-in
# viewer/player and can't run scripts on the repository's origin. Without this, an uploaded HTML or SVG
# file would be served inline from the repository's own origin.
MIMETYPE_WHITELIST = {
    "audio/mpeg",
    "audio/ogg",
    "audio/wav",
    "audio/webm",
    "application/pdf",
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/tiff",
    "text/plain",
    "video/mp4",
    "video/ogg",
    "video/webm",
}
MIMETYPE_PLAINTEXT = {
    "application/javascript",
    "application/json",
    "application/xhtml+xml",
    "application/xml",
    "text/css",
    "text/csv",
    "text/html",
    "image/svg+xml",
}
MIMETYPE_TEXTFILES = {"readme"}

# Same headers invenio-files-rest sends. nginx does NOT pass them through an
# X-Accel-Redirect, so they must also be set with add_header in the internal
# location. Note that Flask-Talisman replaces Content-Security-Policy and
# X-Frame-Options with the app-wide values before the response leaves Flask.
SECURITY_HEADERS = {
    "Content-Security-Policy": "default-src 'none';",
    "X-Content-Type-Options": "nosniff",
    "X-Download-Options": "noopen",
    "X-Permitted-Cross-Domain-Policies": "none",
    "X-Frame-Options": "deny",
    "X-XSS-Protection": "1; mode=block",
}


def parse_prefix_map(value):
    """Parse XSENDFILE_PREFIX_MAP from an environment variable.

    Accepts comma-separated ``storage_root=nginx_prefix`` pairs, for example
    ``/mnt/content=/mnt/content/,/mnt/content1=/mnt/u/content1/``, or the
    same mapping as a JSON object. Spaces and newlines around entries are
    ignored. Returns an empty dict for an empty value.

    Raises ValueError for a malformed value, so a configuration mistake stops
    the application at startup instead of breaking downloads later.
    """
    value = (value or "").strip()
    if not value:
        return {}

    if value.startswith("{"):
        try:
            pairs = json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(f"XSENDFILE_PREFIX_MAP is not valid JSON: {e}") from e
        if not isinstance(pairs, dict):
            raise ValueError("XSENDFILE_PREFIX_MAP JSON must be an object")
        pairs = list(pairs.items())
    else:
        pairs = []
        for entry in value.split(","):
            entry = entry.strip()
            if not entry:
                continue
            root, sep, prefix = entry.partition("=")
            if not sep:
                raise ValueError(
                    f"XSENDFILE_PREFIX_MAP entry {entry!r} must look like "
                    "/storage/root=/nginx/prefix/"
                )
            pairs.append((root.strip(), prefix.strip()))

    prefix_map = {}
    for root, prefix in pairs:
        if not isinstance(root, str) or not root.startswith("/"):
            raise ValueError(
                f"XSENDFILE_PREFIX_MAP storage root {root!r} must be an absolute path"
            )
        if not isinstance(prefix, str) or not prefix.startswith("/"):
            raise ValueError(
                f"XSENDFILE_PREFIX_MAP nginx prefix {prefix!r} for {root} "
                "must start with /"
            )
        prefix_map[root] = prefix
    return prefix_map


def sanitize_mimetype(mimetype, filename=None):
    """Return a mimetype that is safe to serve from the repository origin."""
    if mimetype in MIMETYPE_WHITELIST:
        return mimetype
    if mimetype in MIMETYPE_PLAINTEXT or (
        filename and filename.lower() in MIMETYPE_TEXTFILES
    ):
        return "text/plain"
    return "application/octet-stream"


def local_path_from_uri(uri):
    """Return the normalized filesystem path for a local file URI.

    Accepts plain paths and ``file://`` URIs; raises ``ValueError`` for
    anything else (e.g. ``s3://``).
    """
    if "://" in uri:
        parts = urlsplit(uri)
        if parts.scheme != "file":
            raise ValueError(f"Not a local file URI: {uri}")
        path = parts.path
    else:
        path = uri
    # Collapse leading '//' too: POSIX normpath deliberately keeps it.
    return posixpath.normpath("/" + path.lstrip("/"))


def resolve_redirect_path(real_path, prefix_map):
    """Map a filesystem path to its nginx internal URI, or return None.

    Roots match on whole path components (``/mnt/content`` does not match
    ``/mnt/content1/...``), and the longest root wins for nested roots.
    """
    roots = sorted(
        ((posixpath.normpath(root), prefix) for root, prefix in prefix_map.items()),
        key=lambda item: len(item[0]),
        reverse=True,
    )
    for root, prefix in roots:
        if not real_path.startswith(root.rstrip("/") + "/"):
            continue
        relative = posixpath.relpath(real_path, root)
        return prefix.rstrip("/") + "/" + relative
    return None


def content_disposition(filename, as_attachment):
    """Return (value, options) for a Content-Disposition header."""
    if not as_attachment:
        return "inline", {}
    try:
        filename.encode("ascii")
    except UnicodeEncodeError:
        # Same approach as Flask's send_file: an ASCII fallback first, then
        # the RFC 5987 UTF-8 version that modern browsers prefer.
        options = {}
        simple = (
            unicodedata.normalize("NFKD", filename)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        if simple:
            options["filename"] = simple
        options["filename*"] = "UTF-8''" + quote(filename, safe="!#$&+^`|~")
        return "attachment", options
    return "attachment", {"filename": filename}


def build_xaccel_response(object_version, restricted, as_attachment=False):
    """Build an X-Accel-Redirect response for the given ObjectVersion."""
    real_path = local_path_from_uri(object_version.file.uri)
    prefix_map = current_app.config.get("XSENDFILE_PREFIX_MAP", DEFAULT_PREFIX_MAP)
    redirect = resolve_redirect_path(real_path, prefix_map)
    if redirect is None:
        raise RuntimeError(
            f"No nginx internal-location mapping configured for {real_path}"
        )

    filename = object_version.basename
    mimetype = sanitize_mimetype(getattr(object_version, "mimetype", None), filename)

    response = make_response()
    response.headers["X-Accel-Redirect"] = redirect
    response.headers["Content-Type"] = mimetype

    # Like invenio-files-rest: force a download for unknown types so browsers
    # can't sniff and render them.
    disposition, options = content_disposition(
        filename, as_attachment or mimetype == "application/octet-stream"
    )
    response.headers.set("Content-Disposition", disposition, **options)
    response.headers.update(SECURITY_HEADERS)

    if restricted:
        response.headers["Cache-Control"] = (
            "private, no-cache, no-store, must-revalidate"
        )
    else:
        response.cache_control.public = True
        cache_timeout = current_app.get_send_file_max_age(filename)
        if cache_timeout is not None:
            response.cache_control.max_age = cache_timeout

    return response


def patch_transfer_send_file():
    """Monkeypatch Transfer.send_file to support X-Accel-Redirect.

    Safe to call more than once (InvenioRDM builds both a UI and an API app).
    """
    from invenio_records_resources.services.files.transfer.base import Transfer

    if getattr(Transfer.send_file, "_xaccel_patched", False):
        return

    original_send_file = Transfer.send_file

    def patched_send_file(self, *, restricted, as_attachment=False, **kwargs):
        def fallback():
            return original_send_file(
                self, restricted=restricted, as_attachment=as_attachment, **kwargs
            )

        if not current_app.config.get("FILES_REST_XSENDFILE_ENABLED"):
            return fallback()

        object_version = self.file_record.object_version
        try:
            return build_xaccel_response(
                object_version, restricted, as_attachment=as_attachment
            )
        except Exception:
            current_app.logger.exception(
                "XSendfile: could not build X-Accel response for %s",
                getattr(object_version, "key", object_version),
            )
            size = getattr(getattr(object_version, "file", None), "size", None)
            limit = current_app.config.get(
                "XSENDFILE_FALLBACK_MAX_SIZE", DEFAULT_FALLBACK_MAX_SIZE
            )
            if size is None or size > limit:
                raise InternalServerError(
                    "This file can't be downloaded right now. Please try again later."
                )
            return fallback()

    patched_send_file._xaccel_patched = True
    patched_send_file.__wrapped__ = original_send_file
    Transfer.send_file = patched_send_file


def init_app(app):
    """Entry point for ``invenio_base.finalize_app`` / ``api_finalize_app``."""
    patch_transfer_send_file()
