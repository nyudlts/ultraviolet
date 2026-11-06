# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""E2E tests of what the community "depositor" role allows.

These run against the real application stack (database, search, cache) with
no stubs, and drive it through the REST API as logged-in users.
"""

import os
from http import HTTPStatus

import pytest
from invenio_access.permissions import authenticated_user
from invenio_access.utils import get_identity
from invenio_accounts import testutils
from invenio_accounts.testutils import login_user_via_session
from invenio_communities import current_communities
from invenio_communities.members.records.api import Member
from invenio_search import current_search_client

PASSWORD = "123456"


def community_data(slug):
    return {
        "slug": slug,
        "metadata": {"title": slug},
        # "open" so that the community's own policy never stops a submission:
        # only the rules added by Ultraviolet decide who may submit.
        "access": {
            "visibility": "public",
            "member_policy": "open",
            "record_policy": "open",
            "review_policy": "open",
        },
    }


def add_member(community, user, role):
    Member.create(
        {},
        community_id=community.id,
        user_id=user.id,
        role=role,
        active=True,
        visible=True,
    )


@pytest.fixture()
def people(running_app, search_clear, db, users):
    """The users of the scenario, by name."""
    created = {
        name: testutils.create_test_user(f"{name}@test.com", PASSWORD, active=True)
        for name in (
            "community_a_depositor",
            "community_a_reader",
            "no_roles",
            "community_owner",
        )
    }
    # existing fixture: user4 has the site-wide "depositor" role
    created["site_depositor"] = users["user4"]
    db.session.commit()
    return created


@pytest.fixture()
def communities(people, db):
    """Communities A and B, with a depositor and a reader in A only."""
    community_owner = get_identity(people["community_owner"])
    community_owner.provides.add(authenticated_user)
    a = current_communities.service.create(
        community_owner, community_data("community-a")
    )
    b = current_communities.service.create(
        community_owner, community_data("community-b")
    )
    # Index.refresh() ignores the test index prefix, so refresh everything
    current_search_client.indices.refresh()

    add_member(a._record, people["community_a_depositor"], "depositor")
    add_member(a._record, people["community_a_reader"], "reader")
    db.session.commit()
    return {"a": a.id, "b": b.id}


@pytest.fixture()
def client_for(app, people):
    """Return a client logged in as the named user."""

    def make(name):
        client = app.test_client()
        login_user_via_session(client, email=people[name].email)
        return client

    return make


@pytest.fixture()
def draft_of(minimal_record):
    """Create a draft as the given client; return the response."""

    def create(client):
        return client.post("/api/records", json=minimal_record)

    return create


def submit_for_review(client, draft_id, community_id):
    """Attach the draft to the community and submit it."""
    response = client.put(
        f"/api/records/{draft_id}/draft/review",
        json={"receiver": {"community": community_id}, "type": "community-submission"},
    )
    if response.status_code != HTTPStatus.OK:
        return response
    return client.post(
        f"/api/records/{draft_id}/draft/actions/submit-review",
        json={"payload": {"content": "Please review", "format": "html"}},
    )


def publish(client, draft_id):
    return client.post(f"/api/records/{draft_id}/draft/actions/publish")


#
# Creating records
#
@pytest.mark.skipif(
    os.getenv("E2E", "no") != "yes",
    reason="Skipping E2E tests because E2E environment variable is not set",
)
@pytest.mark.parametrize(
    "name, status",
    [
        pytest.param(
            "community_a_depositor", HTTPStatus.CREATED, id="community depositor"
        ),
        pytest.param("site_depositor", HTTPStatus.CREATED, id="site depositor"),
        pytest.param("community_a_reader", HTTPStatus.FORBIDDEN, id="community reader"),
        pytest.param("no_roles", HTTPStatus.FORBIDDEN, id="no roles"),
    ],
)
def test_who_can_create_a_draft(communities, client_for, draft_of, name, status):
    assert draft_of(client_for(name)).status_code == status


#
# Submitting to a community
#
@pytest.mark.skipif(
    os.getenv("E2E", "no") != "yes",
    reason="Skipping E2E tests because E2E environment variable is not set",
)
def test_community_depositor_submits_for_review(communities, client_for, draft_of):
    community_a_depositor = client_for("community_a_depositor")
    draft_id = draft_of(community_a_depositor).json["id"]

    response = submit_for_review(community_a_depositor, draft_id, communities["a"])

    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json["status"] == "submitted"
    # waiting for review, so not published yet
    assert (
        client_for("no_roles").get(f"/api/records/{draft_id}").status_code
        == HTTPStatus.NOT_FOUND
    )


@pytest.mark.skipif(
    os.getenv("E2E", "no") != "yes",
    reason="Skipping E2E tests because E2E environment variable is not set",
)
def test_community_depositor_cannot_submit_to_another_community(
    communities, client_for, draft_of
):
    community_a_depositor = client_for("community_a_depositor")
    draft_id = draft_of(community_a_depositor).json["id"]

    response = submit_for_review(community_a_depositor, draft_id, communities["b"])

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.skipif(
    os.getenv("E2E", "no") != "yes",
    reason="Skipping E2E tests because E2E environment variable is not set",
)
def test_site_depositor_can_submit_to_any_community(communities, client_for, draft_of):
    site_depositor = client_for("site_depositor")
    draft_id = draft_of(site_depositor).json["id"]

    response = submit_for_review(site_depositor, draft_id, communities["b"])

    assert response.status_code == HTTPStatus.ACCEPTED


#
# Publishing
#
@pytest.mark.skipif(
    os.getenv("E2E", "no") != "yes",
    reason="Skipping E2E tests because E2E environment variable is not set",
)
def test_community_depositor_cannot_publish_outside_a_community(
    communities, client_for, draft_of
):
    community_a_depositor = client_for("community_a_depositor")
    draft_id = draft_of(community_a_depositor).json["id"]

    assert publish(community_a_depositor, draft_id).status_code == HTTPStatus.FORBIDDEN


@pytest.mark.skipif(
    os.getenv("E2E", "no") != "yes",
    reason="Skipping E2E tests because E2E environment variable is not set",
)
def test_site_depositor_can_still_publish_outside_a_community(
    communities, client_for, draft_of
):
    site_depositor = client_for("site_depositor")
    draft_id = draft_of(site_depositor).json["id"]

    assert publish(site_depositor, draft_id).status_code == HTTPStatus.ACCEPTED


@pytest.mark.skipif(
    os.getenv("E2E", "no") != "yes",
    reason="Skipping E2E tests because E2E environment variable is not set",
)
def test_accepting_the_request_publishes_the_record(communities, client_for, draft_of):
    community_a_depositor = client_for("community_a_depositor")
    draft_id = draft_of(community_a_depositor).json["id"]
    request_id = submit_for_review(
        community_a_depositor, draft_id, communities["a"]
    ).json["id"]

    accepted = client_for("community_owner").post(
        f"/api/requests/{request_id}/actions/accept", json={}
    )

    assert accepted.status_code == HTTPStatus.OK
    assert (
        client_for("no_roles").get(f"/api/records/{draft_id}").status_code
        == HTTPStatus.OK
    )
