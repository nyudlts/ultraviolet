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
from flask_security import login_user
from flask_security.utils import hash_password
from invenio_access.models import ActionUsers
from invenio_access.proxies import current_access
from invenio_accounts.proxies import current_datastore
from invenio_accounts.testutils import login_user_via_session
from invenio_db import db


# modify application configuration
@pytest.fixture(scope="module")
def app_config(app_config, ultraviolet_instance_path):
    # need this to make sure separate indexes and database are created for testing
    app_config["SEARCH_INDEX_PREFIX"] = "test"
    app_config["SEARCH_INDEX_PREFIX"] = "test"
    app_config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://nyudatarepository:changeme@localhost/test_uv"
    return app_config


# overriding instance path allows us to make sure we use ultraviolet templates
@pytest.fixture(scope="module")
def ultraviolet_instance_path():
    return os.path.join(sys.prefix, "var", "instance")

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
def roles(app, db):
    """Create some roles."""
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore
        role1 = datastore.create_role(name="admin", description="admin role")
        role2 = datastore.create_role(name="test", description="tests are coming")

    db.session.commit()
    return {"admin": role1, "test": role2}


@pytest.fixture()
def admin_user(users, roles):
    """Give admin rights to a user."""
    user = users["user1"]
    current_datastore.add_role_to_user(user,"admin" )
    action = current_access.actions["superuser-access"]
    db.session.add(ActionUsers.allow(action, user_id=user.id))

    return user


@pytest.fixture()
def client_with_login(client, users):
    """Log in a user to the client."""
    user = users["user1"]
    login_user(user, remember=True)
    login_user_via_session(client, email=user.email)
    return client