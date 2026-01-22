# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Tests for restricted file message on record page."""
import pytest
from invenio_access.permissions import system_identity
from invenio_communities import current_communities
from invenio_rdm_records.proxies import current_rdm_records_service, current_record_communities_service
from invenio_search import current_search_client


@pytest.fixture()
def restricted_record():
    return {
        "pids": {},
        "access": {
            "record": "restricted",
            "files": "restricted",
        },
        "files": {
            "enabled": False,
        },
        "metadata": {
            "publication_date": "2020-06-01",
            "resource_type": {"id": "image-photo"},
            "creators": [{
                "person_or_org": {
                    "name": "Troy Inc.",
                    "type": "organizational",
                },
            }],
            "publisher": "Acme Inc",
            "title": "A Romans story",
        }
    }


@pytest.fixture(scope="module")
def communities_index():
    if not current_search_client.indices.exists(index="communities-communities-v2.0.0"):
        current_search_client.indices.create(index="communities-communities-v2.0.0")


def test_user_without_special_role_cannot_access_restricted_records(services, app, db, client_with_login,
                                                                    restricted_record):
    draft = current_rdm_records_service.create(system_identity, restricted_record.copy())
    record = current_rdm_records_service.publish(system_identity, draft.id)

    response = client_with_login.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })

    assert 403 == response.status_code


def test_anonymous_user_cannot_access_restricted_records(services, app, db, base_client, restricted_record):
    draft = current_rdm_records_service.create(system_identity, restricted_record.copy())
    record = current_rdm_records_service.publish(system_identity, draft.id)

    response = base_client.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })

    assert 403 == response.status_code


def test_user_with_nyu_role_can_access_restricted_records(services, app, client_with_nyu_login, restricted_record):
    draft = current_rdm_records_service.create(system_identity, restricted_record.copy())
    record = current_rdm_records_service.publish(system_identity, draft.id)

    response = client_with_nyu_login.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })

    assert 200 == response.status_code


def test_user_without_community_access_cannot_see_restricted_records(services, app, db, base_client, restricted_record,
                                                                     communities_index):
    draft = current_rdm_records_service.create(identity=system_identity, data=(restricted_record.copy()))
    record = current_rdm_records_service.publish(system_identity, draft.id)

    community = current_communities.service.create(
        identity=system_identity,
        data={
            "access": {
                "visibility": "restricted",
                "members_visibility": "restricted",
                "record_submission_policy": "open",
            },
            "slug": "community1",
            "metadata": {
                "title": "Test Community",
            },
        })

    current_record_communities_service.add(
        system_identity,
        record["id"],
        {"communities": [{"id": community.id}]}
    )

    response = base_client.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })

    assert 403 == response.status_code


def test_user_with_community_access_can_see_restricted_records(services, app, db, client_with_basic_user, users,
                                                               restricted_record, communities_index):
    draft = current_rdm_records_service.create(identity=system_identity, data=(restricted_record.copy()))
    record = current_rdm_records_service.publish(system_identity, draft.id)

    community = current_communities.service.create(
        identity=system_identity,
        data={
            "access": {
                "visibility": "restricted",
                "members_visibility": "restricted",
                "record_submission_policy": "open",
            },
            "slug": "community1",
            "metadata": {
                "title": "Test Community",
            },
        })

    current_communities.service.members.add(
        system_identity,
        community.id,
        {
            "members": [{"type": "user", "id": str(users["user5"].id)}],
            "role": "reader"
        }
    )

    current_record_communities_service.add(
        system_identity,
        record["id"],
        {"communities": [{"id": community.id}]}
    )

    response = client_with_basic_user.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })

    assert 200 == response.status_code
