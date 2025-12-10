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

from invenio_access.permissions import system_identity
from invenio_communities import current_communities
from invenio_communities.communities.records.api import Community
from invenio_rdm_records.proxies import current_rdm_records_service, current_record_communities_service
from invenio_search import current_search_client


def test_user_without_special_role_cannot_access_restricted_records(services, app, db, client_with_login):
    service = current_rdm_records_service

    data = {
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
                    "family_name": "Brown",
                    "given_name": "Troy",
                    "type": "personal"
                }
            }, {
                "person_or_org": {
                    "name": "Troy Inc.",
                    "type": "organizational",
                },
            }],
            # because DATACITE_ENABLED is True, this field is required
            "publisher": "Acme Inc",
            "title": "A Romans story",
        }
    }

    draft = service.create(system_identity, data)
    record = service.publish(system_identity, draft.id)

    response = client_with_login.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })
    assert 403 == response.status_code


def test_anonymous_user_cannot_access_restricted_records(services, app, db, base_client):
    service = current_rdm_records_service

    data = {
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
                    "family_name": "Brown",
                    "given_name": "Troy",
                    "type": "personal"
                }
            }, {
                "person_or_org": {
                    "name": "Troy Inc.",
                    "type": "organizational",
                },
            }],
            "publication_date": "2020-06-01",
            # because DATACITE_ENABLED is True, this field is required
            "publisher": "Acme Inc",
            "resource_type": {"id": "image-photo"},
            "title": "A Romans story",
        }
    }

    draft = service.create(system_identity, data)
    record = service.publish(system_identity, draft.id)

    response = base_client.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })
    assert 403 == response.status_code


def test_user_with_nyu_role_can_access_restricted_records(services, app, client_with_nyu_login):
    service = current_rdm_records_service

    data = {
        "pids": {},
        "access": {
            "record": "restricted",
            "files": "restricted"
        },
        "files": {
            "enabled": False,
        },
        "metadata": {
            "publication_date": "2020-06-01",
            "resource_type": {"id": "image-photo"},
            "creators": [{
                "person_or_org": {
                    "family_name": "Brown",
                    "given_name": "Troy",
                    "type": "personal"
                }
            }, {
                "person_or_org": {
                    "name": "Troy Inc.",
                    "type": "organizational",
                },
            }],
            "publication_date": "2020-06-01",
            # because DATACITE_ENABLED is True, this field is required
            "publisher": "Acme Inc",
            "resource_type": {"id": "image-photo"},
            "title": "A Romans story",
        }
    }

    draft = service.create(system_identity, data)
    record = service.publish(system_identity, draft.id)

    response = client_with_nyu_login.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })

    assert 200 == response.status_code


# Specifically, I’d like to verify that when a record contains a restricted
# file and is assigned to a community, anonymous users can not see it but users
# who belong to that community’s reader group are able to view the file. Since
# we have customized permission policies, we want to ensure they don't interfere
# with the default community access rules.

def test_user_without_community_access_cannot_see_restricted_records(services, app, db, base_client):
    if not current_search_client.indices.exists(index="communities-communities-v2.0.0"):
        current_search_client.indices.create(index="communities-communities-v2.0.0")

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

    draft = current_rdm_records_service.create(
        identity=system_identity,
        data={
            "pids": {},
            "access": {
                "record": "restricted",
                "files": "restricted"
            },
            "files": {
                "enabled": False,
            },
            "metadata": {
                "publication_date": "2020-06-01",
                "resource_type": {"id": "image-photo"},
                "creators": [{
                    "person_or_org": {
                        "family_name": "Brown",
                        "given_name": "Troy",
                        "type": "personal"
                    }
                }, {
                    "person_or_org": {
                        "name": "Troy Inc.",
                        "type": "organizational",
                    },
                }],
                "publication_date": "2020-06-01",
                "publisher": "Acme Inc",
                "resource_type": {"id": "image-photo"},
                "title": "A Romans story",
            }
        })
    record = current_rdm_records_service.publish(system_identity, draft.id)

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


def test_user_with_community_access_can_see_restricted_records(services, app, db, client_with_basic_user, users):
    if not current_search_client.indices.exists(index="communities-communities-v2.0.0"):
        current_search_client.indices.create(index="communities-communities-v2.0.0")

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

    draft = current_rdm_records_service.create(
        identity=system_identity,
        data={
            "pids": {},
            "access": {
                "record": "restricted",
                "files": "restricted"
            },
            "files": {
                "enabled": False,
            },
            "metadata": {
                "publication_date": "2020-06-01",
                "resource_type": {"id": "image-photo"},
                "creators": [{
                    "person_or_org": {
                        "family_name": "Brown",
                        "given_name": "Troy",
                        "type": "personal"
                    }
                }, {
                    "person_or_org": {
                        "name": "Troy Inc.",
                        "type": "organizational",
                    },
                }],
                "publication_date": "2020-06-01",
                "publisher": "Acme Inc",
                "resource_type": {"id": "image-photo"},
                "title": "A Romans story",
            }
        })
    record = current_rdm_records_service.publish(system_identity, draft.id)

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
