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
from invenio_rdm_records.proxies import current_rdm_records_service


@pytest.mark.skip(reason="Struggling with test setup")
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
            "publication_date": "2020-06-01",
            # because DATACITE_ENABLED is True, this field is required
            "publisher": "Acme Inc",
            "resource_type": {"id": "image-photo"},
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


@pytest.mark.skip(reason="Struggling with test setup")
def test_user_with_nyu_role_can_access_restricted_records(services, app, client_with_nyu_login):
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

    response = client_with_nyu_login.get("/api/records/" + record['id'], headers={
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    })
    assert 200 == response.status_code
