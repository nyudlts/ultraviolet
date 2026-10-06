# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Tests for the X-Accel-Redirect helper functions."""

import pytest
from werkzeug.datastructures import Headers
from werkzeug.http import parse_options_header

from ultraviolet.xsendfile import (
    DEFAULT_PREFIX_MAP,
    content_disposition,
    local_path_from_uri,
    parse_prefix_map,
    resolve_redirect_path,
    sanitize_mimetype,
)


def _disposition_header(filename, as_attachment):
    """Build a Content-Disposition header the way the response does."""
    value, options = content_disposition(filename, as_attachment)
    headers = Headers()
    headers.set("Content-Disposition", value, **options)
    return headers["Content-Disposition"]


@pytest.mark.parametrize(
    "path, expected",
    [
        ("/mnt/content/d6/5e/abc/data", "/mnt/content/d6/5e/abc/data"),
        ("/mnt/content1/d6/5e/abc/data", "/mnt/u/content1/d6/5e/abc/data"),
        ("/mnt/test_dir/aa/bb/data", "/mnt/test_dir/aa/bb/data"),
    ],
)
def test_resolve_each_storage_root(path, expected):
    """
    Each configured storage root is mapped to its nginx internal location.
    """
    assert resolve_redirect_path(path, DEFAULT_PREFIX_MAP) == expected


def test_sibling_root_is_not_matched_by_prefix():
    """
    Files under /mnt/content1 must not be mapped to /mnt/content.
    A plain startswith() check produced "/mnt/content/../content1/...",
    which nginx rejects.
    """
    result = resolve_redirect_path("/mnt/content1/d6/5e/abc/data", DEFAULT_PREFIX_MAP)
    assert result == "/mnt/u/content1/d6/5e/abc/data"
    assert ".." not in result


def test_unrelated_directory_is_not_mapped():
    """
    A directory whose name only starts with a storage root is not mapped.
    """
    assert resolve_redirect_path("/mnt/contentX/a/data", DEFAULT_PREFIX_MAP) is None


def test_storage_root_itself_is_not_mapped():
    """
    The storage root is a directory, not a file, so it is not mapped.
    """
    assert resolve_redirect_path("/mnt/content", DEFAULT_PREFIX_MAP) is None


def test_longest_root_wins_for_nested_roots():
    """
    When one storage root is inside another, the more specific one is used.
    """
    prefix_map = {"/mnt/content": "/a/", "/mnt/content/big": "/b/"}
    assert resolve_redirect_path("/mnt/content/big/x/data", prefix_map) == "/b/x/data"
    assert resolve_redirect_path("/mnt/content/x/data", prefix_map) == "/a/x/data"


def test_prefix_without_trailing_slash():
    """
    nginx prefixes work with or without a trailing slash.
    """
    assert resolve_redirect_path("/data/x/y", {"/data": "/files"}) == "/files/x/y"


@pytest.mark.parametrize(
    "uri, expected",
    [
        ("/mnt/content/d6/5e/abc/data", "/mnt/content/d6/5e/abc/data"),
        ("/mnt/content//d6/5e/abc/data", "/mnt/content/d6/5e/abc/data"),
        ("//mnt/content/d6/abc/data", "/mnt/content/d6/abc/data"),
        ("file:///mnt/content/d6/abc/data", "/mnt/content/d6/abc/data"),
        ("/mnt/content/d6/../d7/abc/data", "/mnt/content/d7/abc/data"),
    ],
)
def test_local_path_is_normalized(uri, expected):
    """
    File URIs are normalized before they are mapped.
    """
    assert local_path_from_uri(uri) == expected


def test_non_local_uri_is_rejected():
    """
    Files that are not on local storage can't be served by nginx.
    """
    with pytest.raises(ValueError):
        local_path_from_uri("s3://bucket/d6/abc/data")


def test_path_outside_storage_root_is_not_mapped():
    """
    A path that leaves the storage root with '..' is not mapped.
    """
    path = local_path_from_uri("/mnt/content/../../etc/passwd")
    assert path == "/etc/passwd"
    assert resolve_redirect_path(path, DEFAULT_PREFIX_MAP) is None


@pytest.mark.parametrize(
    "mimetype, filename, expected",
    [
        ("image/png", "a.png", "image/png"),
        ("text/plain", "a.txt", "text/plain"),
        ("application/pdf", "a.pdf", "application/pdf"),
        ("video/mp4", "a.mp4", "video/mp4"),
        ("video/webm", "a.webm", "video/webm"),
        ("text/html", "a.html", "text/plain"),
        ("image/svg+xml", "a.svg", "text/plain"),
        ("application/zip", "a.zip", "application/octet-stream"),
        (None, "a.z01", "application/octet-stream"),
        ("application/x-unknown", "README", "text/plain"),
    ],
)
def test_sanitize_mimetype(mimetype, filename, expected):
    """
    Types that browsers could run as scripts are never served as-is.
    """
    assert sanitize_mimetype(mimetype, filename) == expected


def test_disposition_inline():
    """
    Files that are not downloads are shown inline.
    """
    assert _disposition_header("test.pdf", as_attachment=False) == "inline"


def test_disposition_ascii_filename():
    """
    ASCII file names are sent as a plain filename parameter.
    """
    value, options = parse_options_header(
        _disposition_header("test-file-2.txt", as_attachment=True)
    )
    assert value == "attachment"
    assert options["filename"] == "test-file-2.txt"


def test_disposition_filename_with_quotes_and_semicolon():
    """
    Quotes and semicolons in file names are escaped correctly.
    """
    name = 'my "final" data; v2.csv'
    _, options = parse_options_header(_disposition_header(name, as_attachment=True))
    assert options["filename"] == name


def test_disposition_non_ascii_filename():
    """
    Non-ASCII file names get an ASCII fallback and a UTF-8 filename* version.
    """
    header = _disposition_header("résumé €.txt", as_attachment=True)
    assert "filename*=UTF-8''r%C3%A9sum%C3%A9%20%E2%82%AC.txt" in header
    header.encode("latin-1")  # must be a valid header value
    _, options = parse_options_header(header)
    assert options["filename"] == "résumé €.txt"


def test_parse_prefix_map_pairs():
    """
    The environment variable lists storage_root=nginx_prefix pairs.
    """
    value = "/mnt/content=/mnt/content/,/mnt/content1=/mnt/u/content1/"
    assert parse_prefix_map(value) == {
        "/mnt/content": "/mnt/content/",
        "/mnt/content1": "/mnt/u/content1/",
    }


def test_parse_prefix_map_ignores_spaces_and_newlines():
    """
    Spaces, newlines and a trailing comma are allowed.
    """
    value = """
        /mnt/content = /mnt/content/,
        /mnt/test_dir = /mnt/test_dir/,
    """
    assert parse_prefix_map(value) == {
        "/mnt/content": "/mnt/content/",
        "/mnt/test_dir": "/mnt/test_dir/",
    }


def test_parse_prefix_map_json():
    """
    The same mapping can be given as JSON.
    """
    value = '{"/mnt/content": "/mnt/content/", "/mnt/content1": "/mnt/u/content1/"}'
    assert parse_prefix_map(value) == {
        "/mnt/content": "/mnt/content/",
        "/mnt/content1": "/mnt/u/content1/",
    }


@pytest.mark.parametrize("value", [None, "", "   "])
def test_parse_prefix_map_empty(value):
    """
    An unset or empty variable gives an empty mapping.
    """
    assert parse_prefix_map(value) == {}


@pytest.mark.parametrize(
    "value",
    [
        "/mnt/content",  # no "="
        "mnt/content=/mnt/content/",  # relative storage root
        "/mnt/content=mnt/content/",  # prefix without leading /
        '{"/mnt/content": ',  # broken JSON
        '["/mnt/content"]',  # JSON that isn't an object
    ],
)
def test_parse_prefix_map_rejects_mistakes(value):
    """
    Malformed values raise an error at startup instead of breaking downloads.
    """
    with pytest.raises(ValueError):
        parse_prefix_map(value)


def test_parsed_map_resolves_paths():
    """
    A map read from the environment works for path resolution.
    """
    prefix_map = parse_prefix_map(
        "/mnt/content=/mnt/content/,/mnt/content1=/mnt/u/content1/"
    )
    assert resolve_redirect_path("/mnt/content1/d6/abc/data", prefix_map) == (
        "/mnt/u/content1/d6/abc/data"
    )
