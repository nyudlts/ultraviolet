# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Tests for file downloads handed off to nginx with X-Accel-Redirect.

Tests that take the ``route`` fixture run twice: once through the UI
download link (/records/<id>/files/<key>) and once through the REST API
(/api/records/<id>/files/<key>/content).
"""

import os

import pytest
from invenio_records_resources.services.files.transfer.base import Transfer

from ultraviolet.xsendfile import SECURITY_HEADERS, patch_transfer_send_file

# Flask-Talisman (APP_DEFAULT_SECURE_HEADERS) replaces these on every response
# from the app, so they can't be checked here. In production they come from
# add_header in the nginx internal location, since nginx doesn't pass these
# headers through an X-Accel-Redirect.
APP_WIDE_HEADERS = {"Content-Security-Policy", "X-Frame-Options"}

#
# Both routes
#


def test_file_is_handed_to_nginx(
    route,
    file_url,
    base_client,
    running_app,
    nginx_prefix,
    publish_with_file,
    xsendfile,
):
    """
    The response has an empty body and an X-Accel-Redirect header that
    points at the stored file.
    """
    xsendfile()
    record = publish_with_file("test.pdf")

    response = base_client.get(file_url(record, "test.pdf"))

    assert 200 == response.status_code
    assert b"" == response.data
    redirect = response.headers["X-Accel-Redirect"]
    assert redirect.startswith(nginx_prefix)
    assert redirect.endswith("/data")

    # The redirect must lead nginx to the actual file on disk
    on_disk = os.path.join(running_app.location.uri, redirect[len(nginx_prefix) :])
    with open(on_disk, "rb") as f:
        assert b"test file" == f.read()

    assert "application/pdf" == response.headers["Content-Type"]
    for name, value in SECURITY_HEADERS.items():
        if name not in APP_WIDE_HEADERS:
            assert value == response.headers[name]


def test_file_streams_when_disabled(
    route, file_url, base_client, publish_with_file, xsendfile
):
    """
    With FILES_REST_XSENDFILE_ENABLED off, InvenioRDM streams the file itself.
    """
    xsendfile(enabled=False)
    record = publish_with_file("test.pdf")

    response = base_client.get(file_url(record, "test.pdf"))

    assert 200 == response.status_code
    assert "X-Accel-Redirect" not in response.headers
    assert b"test file" == response.data


@pytest.mark.parametrize(
    "key, mimetype",
    [("test.pdf", "application/pdf"), ("clip.mp4", "video/mp4")],
)
def test_pdf_and_video_open_inline(
    route, file_url, base_client, publish_with_file, xsendfile, key, mimetype
):
    """
    PDFs and videos keep their type and open in the browser, so the
    previewers and direct links work.
    """
    xsendfile()
    record = publish_with_file(key)

    response = base_client.get(file_url(record, key))

    assert 200 == response.status_code
    assert mimetype == response.headers["Content-Type"]
    assert "inline" == response.headers["Content-Disposition"]


def test_html_file_is_served_as_plain_text(
    route, file_url, base_client, publish_with_file, xsendfile
):
    """
    An uploaded HTML file is not served as HTML, so its scripts can't run
    on the repository's domain.
    """
    xsendfile()
    record = publish_with_file("page.html", content=b"<script>alert(1)</script>")

    response = base_client.get(file_url(record, "page.html"))

    assert response.headers["Content-Type"].startswith("text/plain")
    assert "nosniff" == response.headers["X-Content-Type-Options"]


def test_unknown_type_is_sent_as_attachment(
    route, file_url, base_client, publish_with_file, xsendfile
):
    """
    Files of unknown type are always sent as a download, even without
    ?download=1.
    """
    xsendfile()
    record = publish_with_file("data.z01")

    response = base_client.get(file_url(record, "data.z01"))

    assert "application/octet-stream" == response.headers["Content-Type"]
    assert "attachment; filename=data.z01" == response.headers["Content-Disposition"]


def test_anonymous_user_cannot_get_restricted_file(
    route, file_url, base_client, publish_with_file, xsendfile
):
    """
    Permissions are still checked by InvenioRDM before nginx is involved.
    The UI sends anonymous users to the login page; the API returns 403.
    """
    xsendfile()
    record = publish_with_file("test.pdf", files_access="restricted")

    response = base_client.get(file_url(record, "test.pdf"))

    expected = {"ui": (302, 401), "api": (403,)}[route]
    assert response.status_code in expected
    assert "X-Accel-Redirect" not in response.headers


def test_nyu_user_gets_restricted_file_in_nyu_community(
    route,
    file_url,
    client_in_nyu_group,
    nyu_community,
    nginx_prefix,
    publish_with_file,
    xsendfile,
):
    """
    A user in the NYU group can download restricted files of a record in a
    community where the group is a reader. The file comes through nginx and
    the response must not be cached.
    """
    xsendfile()
    record = publish_with_file(
        "test.pdf", files_access="restricted", community=nyu_community
    )

    response = client_in_nyu_group.get(file_url(record, "test.pdf"))

    assert 200 == response.status_code
    assert response.headers["X-Accel-Redirect"].startswith(nginx_prefix)
    cache_control = response.headers["Cache-Control"]
    assert "private" in cache_control
    assert "no-store" in cache_control
    assert "public" not in cache_control


def test_nyu_user_cannot_get_restricted_file_outside_nyu_community(
    route, file_url, client_in_nyu_group, nyu_community, publish_with_file, xsendfile
):
    """
    Being in the NYU group is not enough by itself: the record must be in
    a community the group belongs to.
    """
    xsendfile()
    record = publish_with_file("test.pdf", files_access="restricted")

    response = client_in_nyu_group.get(file_url(record, "test.pdf"))

    assert 403 == response.status_code
    assert "X-Accel-Redirect" not in response.headers


def test_non_nyu_user_cannot_get_restricted_file_in_nyu_community(
    route,
    file_url,
    client_not_in_nyu_group,
    nyu_community,
    publish_with_file,
    xsendfile,
):
    """
    A logged-in user outside the NYU group can't download restricted files
    from the community.
    """
    xsendfile()
    record = publish_with_file(
        "test.pdf", files_access="restricted", community=nyu_community
    )

    response = client_not_in_nyu_group.get(file_url(record, "test.pdf"))

    assert 403 == response.status_code
    assert "X-Accel-Redirect" not in response.headers


def test_unmapped_small_file_falls_back_to_streaming(
    route, file_url, base_client, nginx_prefix, publish_with_file, xsendfile
):
    """
    If the storage path has no nginx mapping, small files are still served
    by InvenioRDM.
    """
    xsendfile(prefix_map={"/not/a/storage/root": nginx_prefix})
    record = publish_with_file("test.pdf")

    response = base_client.get(file_url(record, "test.pdf"))

    assert 200 == response.status_code
    assert "X-Accel-Redirect" not in response.headers
    assert b"test file" == response.data


def test_unmapped_large_file_is_not_streamed(
    route, file_url, base_client, nginx_prefix, publish_with_file, xsendfile
):
    """
    If the storage path has no nginx mapping, files over the fallback limit
    fail instead of tying up a uWSGI worker.
    """
    xsendfile(prefix_map={"/not/a/storage/root": nginx_prefix}, fallback_max_size=0)
    record = publish_with_file("test.pdf")

    response = base_client.get(file_url(record, "test.pdf"))

    assert 500 == response.status_code
    assert "X-Accel-Redirect" not in response.headers
    assert b"test file" not in response.data


#
# UI download link only
#


def test_ui_download_link_is_attachment(base_client, publish_with_file, xsendfile):
    """
    The UI download button (?download=1) sends the file as a download
    with its file name.
    """
    xsendfile()
    record = publish_with_file("test.pdf")

    response = base_client.get(f"/records/{record['id']}/files/test.pdf?download=1")

    assert 200 == response.status_code
    assert "X-Accel-Redirect" in response.headers
    assert "attachment; filename=test.pdf" == response.headers["Content-Disposition"]


def test_ui_public_file_is_cacheable(base_client, publish_with_file, xsendfile):
    """
    Public files downloaded through the UI can be cached.
    """
    xsendfile()
    record = publish_with_file("test.pdf")

    response = base_client.get(f"/records/{record['id']}/files/test.pdf?download=1")

    assert response.cache_control.public


#
# REST API only
#


def test_api_content_is_never_cached(base_client, publish_with_file, xsendfile):
    """
    The REST API serves every file as restricted, so responses are not
    cached, even for public files.
    """
    xsendfile()
    record = publish_with_file("test.pdf")

    response = base_client.get(f"/api/records/{record['id']}/files/test.pdf/content")

    assert 200 == response.status_code
    assert "X-Accel-Redirect" in response.headers
    cache_control = response.headers["Cache-Control"]
    assert "private" in cache_control
    assert "no-store" in cache_control


#
# The patch itself
#


def test_patch_is_applied_once(app):
    """
    The UI and API apps both apply the patch; it must only wrap send_file once.
    """
    patch_transfer_send_file()
    patched = Transfer.send_file
    patch_transfer_send_file()

    assert Transfer.send_file is patched
    assert Transfer.send_file._xaccel_patched


def test_local_transfer_does_not_bypass_patch(app):
    """
    A local-file transfer class that defines its own send_file would skip
    the patch, and downloads would quietly stream through uWSGI again.
    This catches that after an InvenioRDM upgrade.
    """

    def all_subclasses(cls):
        for sub in cls.__subclasses__():
            yield sub
            yield from all_subclasses(sub)

    overriding = [
        cls.__qualname__
        for cls in all_subclasses(Transfer)
        if "send_file" in vars(cls) and "local" in cls.__qualname__.lower()
    ]
    assert [] == overriding
