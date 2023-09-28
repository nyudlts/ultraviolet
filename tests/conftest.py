# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
# conftest.py
"""Pytest fixtures for ultraviolet testing"""


import sys
import pytest
import os

from flask_principal import AnonymousIdentity
from flask_security import login_user
from flask_security.utils import hash_password
from invenio_access.models import ActionUsers
from invenio_access.proxies import current_access
from invenio_accounts.proxies import current_datastore
from invenio_accounts.testutils import login_user_via_session
from invenio_communities import current_communities
from invenio_communities.communities.records.api import Community
from invenio_access.permissions import any_user as any_user_need, system_identity
from invenio_search import current_search, current_search_client
from invenio_db import db


# modify application configuration
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_rdm_records.records import RDMRecord, RDMDraft
from invenio_records_resources.proxies import current_service_registry
from invenio_requests import current_requests_service, current_events_service
from invenio_vocabularies.contrib.subjects.api import Subject
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_vocabularies.records.api import Vocabulary
from invenio_vocabularies.records.models import VocabularyScheme



@pytest.fixture(scope="module")
def app_config( app_config, ultraviolet_instance_path):
    # need this to make sure separate indexes and database are created for testing
    app_config["SEARCH_INDEX_PREFIX"] = "test-"
    app_config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://nyudatarepository:changeme@localhost/test_uv"

    return app_config


# overriding instance path allows us to make sure we use ultraviolet templates
@pytest.fixture(scope="module")
def ultraviolet_instance_path():
    return os.path.join(sys.prefix, "var", "instance")

#
# Services
#
@pytest.fixture(scope="module")
def community_service(app, app_config):
    """Community service."""
    Community.index.create()
    return current_communities.service

@pytest.fixture(scope="function")
def member_service(community_service):
    """Members subservice."""
    return community_service.members


@pytest.fixture(scope="function")
def requests_service(app):
    """Requests service."""
    return current_requests_service

@pytest.fixture(scope="function")
def events_service(app):
    """Requests service."""
    return current_events_service


@pytest.fixture(scope="module")
def vocabularies_service(app, app_config):
    """Vocabularies service."""
    Vocabulary.index.create()
    return vocabulary_service

@pytest.fixture(scope="module")
def anon_identity():
    """A new user."""
    identity = AnonymousIdentity()
    identity.provides.add(any_user_need)
    return identity


@pytest.fixture(scope="function")
def users(app, db):
    """Create users."""
    password = "123456"
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore
        # create users
        hashed_password = hash_password(password)
        user1 = datastore.create_user(
            email="user1@test.com", password=hashed_password, active=True
        )
        user2 = datastore.create_user(
            email="user2@test.com", password=hashed_password, active=True
        )
        # Give role to admin
        db.session.add(ActionUsers(action="admin-access", user=user1))
    db.session.commit()
    return {
        "user1": user1,
        "user2": user2,
    }


@pytest.fixture(scope="function")
def roles(app, db):
    """Create some roles."""
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore
        role1 = datastore.create_role(name="admin", description="admin role")
        role2 = datastore.create_role(name="test", description="tests are coming")

    db.session.commit()
    return {"admin": role1, "test": role2}


@pytest.fixture(scope="function")
def admin_user(users, roles):
    """Give admin rights to a user."""
    user = users["user1"]
    current_datastore.add_role_to_user(user,"admin" )
    action = current_access.actions["superuser-access"]
    db.session.add(ActionUsers.allow(action, user_id=user.id))

    return user


@pytest.fixture(scope="function")
def client_with_login(client, users):
    """Log in a user to the client."""
    user = users["user1"]
    login_user(user, remember=True)
    login_user_via_session(client, email=user.email)
    return client

@pytest.fixture(scope="module")
def minimal_community():
    """Minimal community metadata."""
    return {
        "access": {
            "visibility": "public",
            "record_policy": "open",
        },
        "slug": "opendata",
        "metadata": {
            "title": "My Community",
        },
    }

@pytest.fixture(scope="function")
def anon_identity():
    """A new user."""
    identity = AnonymousIdentity()
    identity.provides.add(any_user_need)
    return identity

@pytest.fixture(scope="function")
def community_users(UserFixture, app, database):
    """Users."""
    users = {}
    for r in ["owner", "manager", "curator", "reader"]:
        u = UserFixture(
            email=f"{r}@{r}.org",
            password=r,
        )
        u.create(app, database)
        users[r] = u
    # when using `database` fixture (and not `db`), commit the creation of the
    # user because its implementation uses a nested session instead
    database.session.commit()
    return users

@pytest.fixture(scope="function")
def owner(community_users):
    """Community owner user."""
    return community_users["owner"]

@pytest.fixture(scope="function")
def resource_type_type(app, app_config):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "resourcetypes", "rsrct")

@pytest.fixture(scope="function")
def resource_type_item(app, resource_type_type,app_config):
    """Resource type vocabulary record."""
    rst = vocabulary_service.create(
        system_identity,
        {
            "id": "image-photo",
            "icon": "chart bar outline",
            "props": {
                "csl": "graphic",
                "datacite_general": "Image",
                "datacite_type": "Photo",
                "eurepo": "info:eu-repo/semantic/image-photo",
                "openaire_resourceType": "25",
                "openaire_type": "dataset",
                "schema.org": "https://schema.org/Photograph",
                "subtype": "image-photo",
                "type": "image",
            },
            "title": {"en": "Photo"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
    )

@pytest.fixture(scope="function")
def title_type(app,app_config):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "titletypes", "ttyp")


@pytest.fixture(scope="function")
def title_type_item(app, title_type, app_config):
    """Title type vocabulary record."""
    ttyp = vocabulary_service.create(
        system_identity,
        {
            "id": "alternative - title",
            "props": {"datacite": "AlternativeTitle"},
            "title": {"en": "Alternative"},
            "type": "titletypes",
        },
    )
    Vocabulary.index.refresh()

    return ttyp

@pytest.fixture(scope="function")
def creator_role(app, app_config):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "creatorsroles", "crr")

@pytest.fixture(scope="function")
def creator_role_item(app, creator_role, app_config):
    """Title type vocabulary record."""
    crr = vocabulary_service.create(
        system_identity,
        {
            "id": "contactperson",
            "props": {"datacite": "ContactPerson"},
            "title": {"en": "Contact person"},
            "type": "creatorsroles",
        },
    )
    Vocabulary.index.refresh()

    return crr

@pytest.fixture(scope="function")
def contributor_role(app, app_config):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "contributorsroles", "cor")


@pytest.fixture(scope="function")
def contributor_role_item(app, contributor_role, app_config):
    """Title type vocabulary record."""
    cor = vocabulary_service.create(
        system_identity,
        {
            "id": "contactperson",
            "props": {"datacite": "ContactPerson"},
            "title": {"en": "Contact person"},
            "type": "contributorsroles",
        },
    )
    Vocabulary.index.refresh()

    return cor

@pytest.fixture(scope="function")
def relations_type(app, app_config):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "relationtypes", "rlt")


@pytest.fixture(scope="function")
def relations_type_item(app, relations_type, app_config):
    """Title type vocabulary record."""
    rlt = vocabulary_service.create(
        system_identity,
        {
            "id": "iscitedby",
            "props": {"datacite": "IsCitedBy"},
            "title": {"en": "Is cited by"},
            "type": "relationtypes",
        },
    )
    Vocabulary.index.refresh()

    return rlt

@pytest.fixture(scope="function")
def description_type(app, app_config):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "descriptiontypes", "dty")


@pytest.fixture(scope="function")
def description_type_item(app, description_type, app_config):
    """Title type vocabulary record."""
    dty = vocabulary_service.create(
        system_identity,
        {
            "id": "abstract",
            "props": {"datacite": "Abstract"},
            "title": {"en": "Abstract"},
            "type": "descriptiontypes",
        },
    )
    Vocabulary.index.refresh()

    return dty

@pytest.fixture(scope="function")
def date_type(app, app_config):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "datetypes", "dat")


@pytest.fixture(scope="function")
def date_type_item(app, date_type, app_config):
    """Title type vocabulary record."""
    dat = vocabulary_service.create(
        system_identity,
        {
            "id": "created",
            "props": {"datacite": "Created"},
            "title": {"en": "Created"},
            "type": "datetypes",
        },
    )
    Vocabulary.index.refresh()

    return dat

@pytest.fixture(scope="module")
def languages_type(app):
    """Language vocabulary type."""
    return vocabulary_service.create_type(system_identity, "languages", "lng")


@pytest.fixture(scope="function")
def language_item(app, languages_type, app_config):
    """Language vocabulary record."""
    lang = vocabulary_service.create(
        system_identity,
        {
            "id": "eng",
            "props": {
                "alpha_2": "",
            },
            "title": {"en": "English"},
            "type": "languages",
        },
    )
    Vocabulary.index.refresh()

    return lang

@pytest.fixture(scope="function")
def subjects_mesh_scheme(app, db, app_config):
    """Subject Scheme for MeSH."""
    scheme = VocabularyScheme.create(
        id="MeSH",
        parent_id="subjects",
        name="Medical Subject Headings",
        uri="https://www.nlm.nih.gov/mesh/meshhome.html",
    )
    db.session.commit()
    return scheme

@pytest.fixture(scope="function")
def subject_item(app, subjects_mesh_scheme, subjects_service, app_config):
    """Subject vocabulary record."""
    subj = subjects_service.create(
        system_identity,
        {
            "id": "https://id.nlm.nih.gov/mesh/D000015",
            "scheme": "MeSH",
            "subject": "Abnormalities, Multiple",
        },
    )
    Subject.index.refresh()

    return subj

@pytest.fixture(scope="function")
def subjects_service(app, app_config):
    """Subjects service."""
    return current_service_registry.get("subjects")

@pytest.fixture()
def _search_create_indexes(app_config):
    """Create all registered search indexes."""
    to_create = [
        RDMRecord.index._name,
        RDMDraft.index._name,
        Community.index._name,
    ]
    app_config["SEARCH_INDEX_PREFIX"] = "test-"
    # list to trigger iter
    list(current_search.create(ignore_existing=True, index_list=to_create ))
    current_search_client.indices.refresh()

@pytest.fixture()
def _search_delete_indexes():
    """Delete all registered search indexes."""
    to_delete = [
        RDMRecord.index._name,
        RDMDraft.index._name,
        Community.index._name,
    ]
    list(current_search.delete(index_list=to_delete))


# overwrite pytest_invenio.fixture to only delete record indices
# keeping vocabularies.
@pytest.fixture()
def search_clear(search):
    """Clear search indices after test finishes (function scope).

    This fixture rollback any changes performed to the indexes during a test,
    in order to leave search in a clean state for the next test.
    """
    from invenio_search import current_search, current_search_client

    yield search
    _search_delete_indexes(current_search)
    _search_create_indexes(current_search, current_search_client)

@pytest.fixture(scope="function")
def opendata_community( _search_create_indexes, minimal_community, location, db, app_config):
    """A community."""
    slug = "opendata"
    try:
        c = current_communities.service.record_cls.pid.resolve(slug)

    except PIDDoesNotExistError:
        c = current_communities.service.create(
            system_identity,
            minimal_community
        )
        Community.index.refresh()

    return c

