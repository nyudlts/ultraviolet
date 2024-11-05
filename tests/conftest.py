    # app_config["REST_CSRF_ENABLED"] = False
    # app_config['SQLALCHEMY_POOL_TIMEOUT'] = None
    # app_config["VOCABULARIES"] = {
    #     "subjects": {
    #         "pid-type": "sub",
    #     }
    # }
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
from invenio_accounts.proxies import current_datastore
from invenio_access.proxies import current_access

# modify application configuration
@pytest.fixture(scope="module")
def app_config(app_config):
    # sqllite refused to create mock db without those parameters and they are missing
    app_config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": False,
        "pool_recycle": 3600,
    }
    # need this to make sure separate indexes are created for testing
    app_config["SEARCH_INDEX_PREFIX"] = "test"
    app_config["SERVER_NAME"] = "127.0.0.1"
    app_config['MAX_FILE_SIZE'] = 50
    app_config["REST_CSRF_ENABLED"] = False
    return app_config


# overriding instance path allows us to make sure we use ultraviolet templates
@pytest.fixture(scope="module")
def ultraviolet_instance_path():
    return os.path.join(sys.prefix, "var", "instance")

# Copied from https://github.dev/inveniosoftware/invenio-rdm-records/tree/maint-1.3.x/tests/records

# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2022 CERN.
# Copyright (C) 2019-2022 Northwestern University.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

# Monkey patch Werkzeug 2.1
# Flask-Login uses the safe_str_cmp method which has been removed in Werkzeug
# 2.1. Flask-Login v0.6.0 (yet to be released at the time of writing) fixes the
# issue. Once we depend on Flask-Login v0.6.0 as the minimal version in
# Flask-Security-Invenio/Invenio-Accounts we can remove this patch again.
try:
    # Werkzeug <2.1
    from werkzeug import security

    security.safe_str_cmp
except AttributeError:
    # Werkzeug >=2.1
    import hmac

    from werkzeug import security

    security.safe_str_cmp = hmac.compare_digest

from collections import namedtuple
from copy import deepcopy
from datetime import datetime

import pytest
from flask import g
from flask_principal import Identity, Need, UserNeed
from flask_security import login_user, logout_user
from flask_security.utils import hash_password
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access, system_identity
from invenio_accounts.models import Role
from invenio_accounts.testutils import login_user_via_session
from invenio_administration.permissions import administration_access_action

from invenio_cache import current_cache
from invenio_communities import current_communities
from invenio_communities.communities.records.api import Community
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.custom_fields import TextCF
from invenio_vocabularies.contrib.affiliations.api import Affiliation
from invenio_vocabularies.contrib.awards.api import Award
from invenio_vocabularies.contrib.funders.api import Funder
from invenio_vocabularies.contrib.subjects.api import Subject
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_vocabularies.records.api import Vocabulary
from invenio_access.models import ActionUsers



@pytest.fixture(scope="function")
def minimal_record():
    """Minimal record data as dict coming from the external world."""
    return {
        "pids": {},
        "access": {
            "record": "public",
            "files": "public",
        },
        "files": {
            "enabled": False,  # Most tests don't care about files
        },
        "metadata": {
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Brown",
                        "given_name": "Troy",
                        "type": "personal",
                    }
                },
                {
                    "person_or_org": {
                        "name": "Troy Inc.",
                        "type": "organizational",
                    },
                },
            ],
            "publication_date": "2020-06-01",
            # because DATACITE_ENABLED is True, this field is required
            "publisher": "Acme Inc",
            "resource_type": {"id": "image-photo"},
            "title": "A Romans story",
        },
    }


@pytest.fixture()
def client_with_login(client, users):
    """Log in a user to the client."""
    user = users["user1"]
    login_user(user, remember=True)
    login_user_via_session(client, email=user.email)
    return client


@pytest.fixture()
def roles(app, db):
    """Create some roles."""
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore
        role1 = datastore.create_role(name="admin", description="admin role")
        role2 = datastore.create_role(name="test", description="tests are coming")

    db.session.commit()
    return {"admin": role1, "test": role2}


@pytest.fixture(scope="module")
def languages_type(app):
    """Lanuage vocabulary type."""
    return vocabulary_service.create_type(system_identity, "languages", "lng")


@pytest.fixture(scope="module")
def languages_v(app, languages_type):
    """Language vocabulary record."""
    vocabulary_service.create(
        system_identity,
        {
            "id": "dan",
            "title": {
                "en": "Danish",
                "da": "Dansk",
            },
            "props": {"alpha_2": "da"},
            "tags": ["individual", "living"],
            "type": "languages",
        },
    )

    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "eng",
            "title": {
                "en": "English",
                "da": "Engelsk",
            },
            "tags": ["individual", "living"],
            "type": "languages",
        },
    )

    Vocabulary.index.refresh()

    return vocab


@pytest.fixture(scope="module")
def resource_type_type(app):
    """Resource type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "resourcetypes", "rsrct")


@pytest.fixture(scope="module")
def resource_type_v(app, resource_type_type):
    """Resource type vocabulary record."""
    vocabulary_service.create(
        system_identity,
        {
            "id": "dataset",
            "icon": "table",
            "props": {
                "csl": "dataset",
                "datacite_general": "Dataset",
                "datacite_type": "",
                "openaire_resourceType": "21",
                "openaire_type": "dataset",
                "eurepo": "info:eu-repo/semantics/other",
                "schema.org": "https://schema.org/Dataset",
                "subtype": "",
                "type": "dataset",
            },
            "title": {"en": "Dataset"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
    )

    vocabulary_service.create(
        system_identity,
        {  # create base resource type
            "id": "image",
            "props": {
                "csl": "figure",
                "datacite_general": "Image",
                "datacite_type": "",
                "openaire_resourceType": "25",
                "openaire_type": "dataset",
                "eurepo": "info:eu-repo/semantic/other",
                "schema.org": "https://schema.org/ImageObject",
                "subtype": "",
                "type": "image",
            },
            "icon": "chart bar outline",
            "title": {"en": "Image"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
    )

    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "image-photo",
            "props": {
                "csl": "graphic",
                "datacite_general": "Image",
                "datacite_type": "Photo",
                "openaire_resourceType": "25",
                "openaire_type": "dataset",
                "eurepo": "info:eu-repo/semantic/other",
                "schema.org": "https://schema.org/Photograph",
                "subtype": "image-photo",
                "type": "image",
            },
            "icon": "chart bar outline",
            "title": {"en": "Photo"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
    )

    Vocabulary.index.refresh()

    return vocab


@pytest.fixture(scope="module")
def title_type(app):
    """title vocabulary type."""
    return vocabulary_service.create_type(system_identity, "titletypes", "ttyp")


@pytest.fixture(scope="module")
def title_type_v(app, title_type):
    """Title Type vocabulary record."""
    vocabulary_service.create(
        system_identity,
        {
            "id": "subtitle",
            "props": {"datacite": "Subtitle"},
            "title": {"en": "Subtitle"},
            "type": "titletypes",
        },
    )

    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "alternative-title",
            "props": {"datacite": "AlternativeTitle"},
            "title": {"en": "Alternative title"},
            "type": "titletypes",
        },
    )

    Vocabulary.index.refresh()

    return vocab


@pytest.fixture(scope="module")
def description_type(app):
    """title vocabulary type."""
    return vocabulary_service.create_type(system_identity, "descriptiontypes", "dty")


@pytest.fixture(scope="module")
def description_type_v(app, description_type):
    """Title Type vocabulary record."""
    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "methods",
            "title": {"en": "Methods"},
            "props": {"datacite": "Methods"},
            "type": "descriptiontypes",
        },
    )

    Vocabulary.index.refresh()

    return vocab

from invenio_vocabularies import InvenioVocabularies
from invenio_vocabularies.contrib.subjects import SubjectsService
from invenio_vocabularies.contrib.subjects.subjects import record_type
from invenio_search import current_search, current_search_client
@pytest.fixture(scope="module")
def subjects_service(app,):
    """Subjects service fixture with index initialization."""
    # Initialize vocabularies extension
    InvenioVocabularies(app)
    
    # Configure and register the subjects service
    SubjectsServiceConfig = record_type.service_config_cls
    service = SubjectsService(config=SubjectsServiceConfig)
    
    from invenio_records_resources.proxies import current_service_registry
    if "subjects" not in current_service_registry._services:
        current_service_registry.register(service, "subjects")
    
    # Create required indexes
    # list(current_search.create(ignore=[400]))
    current_search_client.indices.refresh()
    




    return service

@pytest.fixture(scope="module")
def subject_v(app, subjects_service):
    """Subject vocabulary record."""
    # subjects_service = current_service_registry.get("subjects")
    vocab = subjects_service.create(
        system_identity,
        {
            "id": "http://id.nlm.nih.gov/mesh/A-D000007",
            "scheme": "MeSH",
            "subject": "Abdominal Injuries",
        },
    )
    if not current_search_client.indices.exists(index="subjects-subject-v1.0.0"):
        current_search_client.indices.create(index="subjects-subject-v1.0.0")
                
    Subject.index.refresh()

    return vocab


@pytest.fixture(scope="module")
def date_type(app):
    """Date vocabulary type."""
    return vocabulary_service.create_type(system_identity, "datetypes", "dat")


@pytest.fixture(scope="module")
def date_type_v(app, date_type):
    """Subject vocabulary record."""
    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "other",
            "title": {"en": "Other"},
            "props": {"datacite": "Other"},
            "type": "datetypes",
        },
    )

    Vocabulary.index.refresh()

    return vocab


@pytest.fixture(scope="module")
def contributors_role_type(app):
    """Contributor role vocabulary type."""
    return vocabulary_service.create_type(system_identity, "contributorsroles", "cor")


@pytest.fixture(scope="module")
def contributors_role_v(app, contributors_role_type):
    """Contributor role vocabulary record."""
    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "other",
            "props": {"datacite": "Other"},
            "title": {"en": "Other"},
            "type": "contributorsroles",
        },
    )

    Vocabulary.index.refresh()

    return vocab


@pytest.fixture(scope="module")
def relation_type(app):
    """Relation type vocabulary type."""
    return vocabulary_service.create_type(system_identity, "relationtypes", "rlt")


@pytest.fixture(scope="module")
def relation_type_v(app, relation_type):
    """Relation type vocabulary record."""
    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "iscitedby",
            "props": {"datacite": "IsCitedBy"},
            "title": {"en": "Is cited by"},
            "type": "relationtypes",
        },
    )

    Vocabulary.index.refresh()

    return vocab


@pytest.fixture(scope="module")
def licenses(app):
    """Licenses vocabulary type."""
    return vocabulary_service.create_type(system_identity, "licenses", "lic")


@pytest.fixture(scope="module")
def licenses_v(app, licenses):
    """Licenses vocabulary record."""
    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "cc-by-4.0",
            "props": {
                "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
                "scheme": "spdx",
                "osi_approved": "",
            },
            "title": {"en": "Creative Commons Attribution 4.0 International"},
            "tags": ["recommended", "all"],
            "description": {
                "en": "The Creative Commons Attribution license allows"
                " re-distribution and re-use of a licensed work on"
                " the condition that the creator is appropriately credited."
            },
            "type": "licenses",
        },
    )

    Vocabulary.index.refresh()

    return vocab


from invenio_vocabularies.contrib.affiliations import AffiliationsService, AffiliationsServiceConfig


@pytest.fixture(scope="module")
def affiliations_v(app):
    """Affiliation vocabulary record."""

    if "affiliations" not in current_service_registry._services:
        service = AffiliationsService(config=AffiliationsServiceConfig())  # Create an instance
        current_service_registry.register(service, "affiliations")


    affiliations_service = current_service_registry.get("affiliations")
    aff = affiliations_service.create(
        system_identity,
        {
            "id": "cern",
            "name": "CERN",
            "acronym": "CERN",
            "identifiers": [
                {
                    "scheme": "ror",
                    "identifier": "01ggx4157",
                },
                {
                    "scheme": "isni",
                    "identifier": "000000012156142X",
                },
            ],
        },
    )
    if not current_search_client.indices.exists(index="affiliations-affiliation-v1.0.0"):
        current_search_client.indices.create(index="affiliations-affiliation-v1.0.0")
                
    Affiliation.index.refresh()

    return aff

from invenio_vocabularies.contrib.funders import FundersService, FundersServiceConfig

@pytest.fixture(scope="module")
def funders_v(app):
    """Funder vocabulary record."""
    if "funders" not in current_service_registry._services:
        service = FundersService(config=FundersServiceConfig())  # Create an instance
        current_service_registry.register(service, "funders")
    
    funders_service = current_service_registry.get("funders")
    funder = funders_service.create(
        identity=system_identity,
        data={
            "id": "00k4n6c32",
            "identifiers": [
                {
                    "identifier": "000000012156142X",
                    "scheme": "isni",
                },
                {
                    "identifier": "00k4n6c32",
                    "scheme": "ror",
                },
            ],
            "name": "European Commission",
            "title": {
                "en": "European Commission",
                "fr": "Commission européenne",
            },
            "country": "BE",
        },
    )
    if not current_search_client.indices.exists(index="funders-funder-v1.0.0"):
        current_search_client.indices.create(index="funders-funder-v1.0.0")
                
    Funder.index.refresh()

    return funder

from invenio_vocabularies.contrib.awards import AwardsService, AwardsServiceConfig

@pytest.fixture(scope="module")
def awards_v(app, funders_v):
    """Funder vocabulary record."""
    if "awards" not in current_service_registry._services:
        service = AwardsService(config=AwardsServiceConfig())  
        current_service_registry.register(service, "awards")
    awards_service = current_service_registry.get("awards")
    award = awards_service.create(
        system_identity,
        {
            "id": "00k4n6c32::755021",
            "identifiers": [
                {
                    "identifier": "https://cordis.europa.eu/project/id/755021",
                    "scheme": "url",
                }
            ],
            "number": "755021",
            "title": {
                "en": (
                    "Personalised Treatment For Cystic Fibrosis Patients With "
                    "Ultra-rare CFTR Mutations (and beyond)"
                ),
            },
            "funder": {"id": "00k4n6c32"},
            "acronym": "HIT-CF",
        },
    )
    if not current_search_client.indices.exists(index="awards-award-v1.0.0"):
        current_search_client.indices.create(index="awards-award-v1.0.0")
                
    Award.index.refresh()

    return award


@pytest.fixture(scope="function")
def cache():
    """Empty cache."""
    try:
        current_cache.clear()
        yield current_cache
    finally:
        current_cache.clear()


RunningApp = namedtuple(
    "RunningApp",
    [
        "app",
        "superuser_identity",
        "location",
        "cache",
        "resource_type_v",
        "subject_v",
        "languages_v",
        "affiliations_v",
        "title_type_v",
        "description_type_v",
        "date_type_v",
        "contributors_role_v",
        "relation_type_v",
        "licenses_v",
        "funders_v",
        "awards_v",
    ],
)


@pytest.fixture
def running_app(
    app,
    superuser_identity,
    location,
    cache,
    resource_type_v,
    subject_v,
    languages_v,
    affiliations_v,
    title_type_v,
    description_type_v,
    date_type_v,
    contributors_role_v,
    relation_type_v,
    licenses_v,
    funders_v,
    awards_v,
):
    """This fixture provides an app with the typically needed db data loaded.

    All of these fixtures are often needed together, so collecting them
    under a semantic umbrella makes sense.
    """
    return RunningApp(
        app,
        superuser_identity,
        location,
        cache,
        resource_type_v,
        subject_v,
        languages_v,
        affiliations_v,
        title_type_v,
        description_type_v,
        date_type_v,
        contributors_role_v,
        relation_type_v,
        licenses_v,
        funders_v,
        awards_v,
    )


@pytest.fixture(scope="function")
def superuser_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="superuser-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=superuser_access, role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


@pytest.fixture(scope="function")
def superuser_identity(admin, superuser_role_need):
    """Superuser identity fixture."""
    identity = admin.identity
    identity.provides.add(superuser_role_need)
    return identity


@pytest.fixture(scope="function")
def admin_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="administration-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=administration_access_action, role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


@pytest.fixture()
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

@pytest.fixture()
def admin_user(users, roles, db):
    """Give admin rights to a user."""
    user = users["user1"]
    current_datastore.add_role_to_user(user,"admin" )
    action = current_access.actions["superuser-access"]
    db.session.add(ActionUsers.allow(action, user_id=user.id))

    return user

@pytest.fixture()
def community_type_type(superuser_identity):
    """Creates and retrieves a language vocabulary type."""
    v = vocabulary_service.create_type(superuser_identity, "communitytypes", "comtyp")
    return v


@pytest.fixture()
def community_type_record(superuser_identity, community_type_type):
    """Creates a d retrieves community type records."""
    record = vocabulary_service.create(
        identity=superuser_identity,
        data={
            "id": "topic",
            "title": {"en": "Topic"},
            "type": "communitytypes",
        },
    )
    Vocabulary.index.refresh()  # Refresh the index

    return record


@pytest.fixture()
def community(running_app, community_type_record, curator, minimal_community):
    """Get the current RDM records service."""
    c = current_communities.service.create(
        curator.identity,
        minimal_community,
    )
    Community.index.refresh()
    return c


@pytest.fixture(scope="session")
def headers():
    """Default headers for making requests."""
    return {
        "content-type": "application/json",
        "accept": "application/json",
    }


@pytest.fixture()
def admin(UserFixture, app, db, admin_role_need):
    """Admin user for requests."""
    u = UserFixture(
        email="admin@inveniosoftware.org",
        password="admin",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "administration-access")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    return u