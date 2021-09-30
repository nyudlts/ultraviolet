# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Tests  to check configuration settings
import os

from invenio_app.factory import create_app


# Check that configuration variables read correctly from os
def test_var_assigned(monkeypatch):
    app_host = "ultraviolet.dlib.nyu.edu"
    db_connection = "postgresql+psycopg2://test:test@somehost.com/test"

    """Mocking setting configuration using environment variables"""
    monkeypatch.setenv("APP_ALLOWED_HOSTS", app_host)
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", db_connection)
    monkeypatch.setenv("SITE_UI_URL", app_host)
    monkeypatch.setenv("SITE_API_URL", app_host + "/api")

    """Create app with configurations passed above"""
    app = create_app()
    assert app.config.get("APP_ALLOWED_HOSTS") == app_host
    assert app.config.get("SQLALCHEMY_DATABASE_URI") == db_connection
    assert app.config.get("SITE_UI_URL") == app_host
    assert app.config.get("SITE_API_URL") == app_host + "/api"


# Check that default values are assign to configuration variables when values are not passed through os
def test_var_noassigned():
    """Mocking using default configuration"""
    app = create_app()
    assert app.config.get("APP_ALLOWED_HOSTS") == ["0.0.0.0", "localhost", "127.0.0.1"]
    assert (
        app.config.get("SQLALCHEMY_DATABASE_URI")
        == "postgresql+psycopg2://nyu-data-repository:nyu-data-repository@localhost/nyu-data-repository"
    )
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_ENABLED") is False
    assert app.config.get("COMMUNITIES_ENABLED") is False
    assert app.config.get("SITE_UI_URL") == "https://127.0.0.1:5000"
    assert app.config.get("SITE_API_URL") == "https://127.0.0.1:5000/api"
