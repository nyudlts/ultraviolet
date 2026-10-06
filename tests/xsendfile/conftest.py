# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
# conftest.py
"""Pytest configuration for X-Accel-Redirect tests."""

from io import BytesIO

import pytest
from flask_security import login_user
from invenio_access.permissions import system_identity
from invenio_accounts.testutils import login_user_via_session
from invenio_communities import current_communities
from invenio_rdm_records.proxies import (
    current_rdm_records_service,
    current_record_communities_service,
)
from invenio_records_resources.proxies import current_service_registry
from invenio_search import current_search_client

from ultraviolet.xsendfile import patch_transfer_send_file

NGINX_PREFIX = "/user_files/"

# Role (group) that login adds NYU users to.
NYU_GROUP = "nyuusers"

# Community role given to the NYU group; "reader" lets members download the
# restricted files of the community's records.
NYU_GROUP_COMMUNITY_ROLE = "reader"

# The same file, through the UI download link and the REST API.
ROUTES = {
    "ui": "/records/{id}/files/{key}",
    "api": "/api/records/{id}/files/{key}/content",
}


@pytest.fixture()
def nginx_prefix():
    """nginx internal location the test storage location is mapped to."""
    return NGINX_PREFIX


@pytest.fixture()
def services(running_app, search_clear):
    """RDM Record Service."""
    return running_app.app.extensions["invenio-rdm-records"].records_service


@pytest.fixture(scope="module")
def file_service(app):
    """Register RDMFileService in the service registry, once per app."""
    existing_service = current_rdm_records_service.draft_files
    if "rdm-files" not in current_service_registry._services:
        current_service_registry.register(existing_service, "rdm-files")
    return existing_service


@pytest.fixture(params=sorted(ROUTES))
def route(request):
    """Run a test once through the UI and once through the REST API."""
    return request.param


@pytest.fixture()
def file_url(route):
    """Return a function that builds the file URL for the current route."""

    def build(record, key, download=False):
        url = ROUTES[route].format(id=record["id"], key=key)
        if download:
            url += "?download=1"
        return url

    return build


def _flask_apps(app):
    """Return the UI app and the API app mounted under /api.

    Both apps have their own config, so settings must be changed on both.
    """
    apps = [app]
    wsgi = app.wsgi_app
    while wsgi is not None and not hasattr(wsgi, "mounts"):
        wsgi = getattr(wsgi, "app", None)
    if wsgi is not None:
        apps.extend(a for a in wsgi.mounts.values() if hasattr(a, "config"))
    return apps


@pytest.fixture()
def xsendfile(app, running_app, services, file_service, monkeypatch):
    """Apply the patch and return a function that configures it.

    The test storage location is mapped to NGINX_PREFIX. Settings are set
    on both the UI and API apps and restored after each test.
    """
    patch_transfer_send_file()

    def configure(enabled=True, prefix_map=None, fallback_max_size=None):
        if prefix_map is None:
            prefix_map = {running_app.location.uri: NGINX_PREFIX}
        for flask_app in _flask_apps(app):
            monkeypatch.setitem(
                flask_app.config, "FILES_REST_XSENDFILE_ENABLED", enabled
            )
            monkeypatch.setitem(flask_app.config, "XSENDFILE_PREFIX_MAP", prefix_map)
            if fallback_max_size is not None:
                monkeypatch.setitem(
                    flask_app.config, "XSENDFILE_FALLBACK_MAX_SIZE", fallback_max_size
                )

    return configure


@pytest.fixture()
def publish_with_file(minimal_record):
    """Return a function that publishes a record with one file.

    If a community is given, the record is added to it.
    """

    def publish(key, content=b"test file", files_access=None, community=None):
        service = current_rdm_records_service

        data = minimal_record.copy()
        data["files"]["enabled"] = True
        if files_access:
            data["access"]["files"] = files_access

        draft = service.create(system_identity, data)
        service.draft_files.init_files(system_identity, draft.id, data=[{"key": key}])
        service.draft_files.set_file_content(
            system_identity, draft.id, key, BytesIO(content)
        )
        service.draft_files.commit_file(system_identity, draft.id, key)

        record = service.publish(system_identity, draft.id)

        if community is not None:
            _, errors = current_record_communities_service.add(
                system_identity,
                record["id"],
                {"communities": [{"id": str(community.id)}]},
            )
            assert not errors, errors

        return record

    return publish


def _login(client, user):
    """Log a user in on the test client, like the client_with_* fixtures."""
    login_user(user, remember=True)
    login_user_via_session(client, email=user.email)
    return client


@pytest.fixture(scope="module")
def communities_index(app):
    """Make sure the communities search index exists."""
    if not current_search_client.indices.exists(index="communities-communities-v2.0.0"):
        current_search_client.indices.create(index="communities-communities-v2.0.0")


@pytest.fixture()
def nyu_user(app, db, users):
    """A user in the NYU group, as after login in production.

    user5 has no other roles, so only the group can grant access.
    """
    datastore = app.extensions["security"].datastore
    role = datastore.find_role(NYU_GROUP) or datastore.create_role(
        name=NYU_GROUP, description="NYU users"
    )
    user = users["user5"]
    datastore.add_role_to_user(user, role)
    db.session.commit()
    return user


@pytest.fixture()
def nyu_community(app, db, communities_index, nyu_user):
    """Public community with the NYU group as a reader, like production.

    The community and its records are public; only the files are restricted.
    Depends on nyu_user so the user is in the group before the group joins
    the community; adding the group refreshes its users' cached memberships.
    """
    community = current_communities.service.create(
        identity=system_identity,
        data={
            "access": {
                "visibility": "public",
                "record_submission_policy": "open",
            },
            "slug": "nyu-restricted",
            "metadata": {
                "title": "NYU restricted community",
            },
        },
    )

    role = app.extensions["security"].datastore.find_role(NYU_GROUP)
    current_communities.service.members.add(
        system_identity,
        community.id,
        {
            "members": [{"type": "group", "id": str(role.id)}],
            "role": NYU_GROUP_COMMUNITY_ROLE,
        },
    )
    return community


@pytest.fixture()
def client_in_nyu_group(client, nyu_user):
    """Client logged in as the NYU group user."""
    return _login(client, nyu_user)


@pytest.fixture()
def client_not_in_nyu_group(client, users):
    """Client logged in as a user with no roles."""
    return _login(client, users["user2"])
