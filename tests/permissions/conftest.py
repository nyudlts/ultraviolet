# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet Permssions is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import os

import flask_security
import pytest
from flask import Flask
from flask_principal import identity_loaded
from invenio_access import InvenioAccess
from invenio_access.loaders import load_permissions_on_identity_loaded
from invenio_access.models import Role
from invenio_accounts import InvenioAccounts
from invenio_accounts.testutils import login_user_via_session
from invenio_communities import InvenioCommunities
from invenio_db import InvenioDB, db
from invenio_files_rest import InvenioFilesREST
from invenio_i18n import InvenioI18N
from invenio_pidstore import InvenioPIDStore
from invenio_records_files import InvenioRecordsFiles
from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets
from invenio_records_rest import InvenioRecordsREST


@pytest.fixture(scope='module')
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture(scope='module')
def base_app():
    """Flask base application fixture."""
    app_ = Flask('testapp')
    app_.config.update(
        ACCOUNTS_USE_CELERY=False,
        SECRET_KEY="CHANGE_ME",
        SECURITY_PASSWORD_SALT="CHANGE_ME_ALSO",
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "SQLALCHEMY_DATABASE_URI", "sqlite:///test.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FILES_REST_DEFAULT_STORAGE_CLASS='S',
        FILES_REST_STORAGE_CLASS_LIST={'A': 'Archive', 'S': 'Standard'},
        FILES_REST_DEFAULT_QUOTA_SIZE=112345789,
        FILES_REST_DEFAULT_MAX_FILE_SIZE=123465789,
        FILES_REST_OBJECT_KEY_MAX_LEN=123456789,
        TESTING=True,
    )
    InvenioDB(app_)
    InvenioI18N(app_)
    InvenioAccounts(app_)
    InvenioCommunities(app_)
    InvenioFilesREST(app_)
    InvenioAccess(app_)
    InvenioRecordsREST(app_)
    InvenioRecordsFiles(app_)
    InvenioPIDStore(app_)
    # UltravioletPermssions(app_)
    return app_


@pytest.fixture(scope='module')
def app(base_app, request):
    """Flask application fixture."""
    with base_app.app_context():
        db.create_all()

    def teardown():
        with base_app.app_context():
            db.drop_all()
            identity_loaded.disconnect(load_permissions_on_identity_loaded)

    request.addfinalizer(teardown)
    return base_app


@pytest.fixture(scope='function')
def user_role(request):
    return request.param


@pytest.fixture(scope='function')
def user_roles_propriatery_record(user_role):
    """Minimal record data as dict coming from the external world."""
    return {
        "pids": {},
        "access": {
            "record": "restricted",
            "files": "restricted",
        },
        "files": {
            "enabled": False,  # Most tests don't care about files
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
            "additional_descriptions": [
                {
                    "description": f"<p>{user_role}</p>",
                    "type": {
                        "id": "technical-info",
                        "title": {
                            "en": "Technical info"
                        }
                    }
                }
            ],
            "title": "A Romans story"
        }
    }


@pytest.fixture(scope='function')
def propriatery_record():
    """Minimal record data as dict coming from the external world."""
    return {
        "pids": {},
        "access": {
            "record": "restricted",
            "files": "restricted",
        },
        "files": {
            "enabled": False,  # Most tests don't care about files
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
            "additional_descriptions": [
                {
                    "description": "<p>nyu</p>",
                    "type": {
                        "id": "technical-info",
                        "title": {
                            "en": "Technical info"
                        }
                    }
                }
            ],
            "title": "A Romans story"
        }
    }


def minimal_headers():
    """Create headers."""
    return {
        'content-type': 'application/octet-stream',
        'accept': 'application/json'
    }


@pytest.fixture(scope='module')
def create_roles(*names):
    """Helper to create roles."""
    roles = []
    for name in names:
        role = Role(name=name)
        db.session.add(role)
        roles.append(role)
    db.session.commit()
    return roles


@pytest.fixture(scope='module')
def assign_roles(user, *roles):
    """Assign roles to users."""
    for user, roles in roles.items():
        for role in roles:
            user.provides.add(role)


def login_user(client, user):
    """Log user in."""
    flask_security.login_user(user, remember=True)
    login_user_via_session(client, email=user.email)


def logout_user(client):
    """Log current user out."""
    flask_security.logout_user()
    with client.session_transaction() as session:
        session.pop("user_id", None)


@pytest.fixture(scope='function')
def create_proprietary_record(client, propriatery_record):
    """Create draft ready for file attachment and return its id."""
    response = client.post("/records", json=propriatery_record, headers=minimal_headers())
    assert response.status_code == 201
    return response.json['id']


@pytest.fixture(scope="session")
def create_record():
    """Factory pattern for a loaded Record.

    The returned dict record has the interface of a Record.

    It provides a default value for each required field.
    """

    def _create_record(metadata=None):
        # TODO: Modify according to record schema
        metadata = metadata or {}
        record = {
            "_access": {
                # TODO: Remove if "access_right" includes it
                "metadata_restricted": False,
                "files_restricted": False,
            },
            "access_right": "open",
            "title": "This is a record",
            "description": "This record is a test record",
            "owners": [1, 2, 3],
            "internal": {
                "access_levels": {},
            },
            "files": {
                "enabled": True,  # Most tests don't care about files
            },

        }
        record.update(metadata)
        return record

    return _create_record


@pytest.fixture(scope="function")
def create_real_record(create_record, location):
    """Factory pattern to create a real Record.

    This is needed for tests relying on database and search engine operations.
    """

    def _create_real_record(bucket, metadata=None):
        record_dict = create_record(metadata)

        record = Record.create(record_dict, with_bucket=False)

        # Create link between record and bucket
        RecordsBuckets.create(record=record.model, bucket=bucket)
        record._bucket = bucket

        return record
        # Flush to index and database
        # current_search.flush_and_refresh(index='*')
        # db.session.commit()

    return _create_real_record


@pytest.fixture()
def services(running_app, search_clear):
    """RDM Record Service."""
    return running_app.app.extensions["invenio-rdm-records"].records_service
