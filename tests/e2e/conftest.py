# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# invenio-nyu is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
# conftest.py


"""Pytest configuration."""


import invenio_app.factory as factory
from invenio_base.wsgi import create_wsgi_factory, wsgi_proxyfix
from invenio_config import create_config_loader
import pytest
import os


@pytest.fixture(scope="module")
def app_config(app_config):
    app_config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": False,
        "pool_recycle": 3600,
    }
    app_config["SEARCH_INDEX_PREFIX"] = "test"
    return app_config


@pytest.fixture(scope="module")
def create_app_e2e():
    create_app_e2e = factory.create_app_factory(
        "invenio",
        config_loader=create_config_loader(config=None, env_prefix="Invenio"),
        blueprint_entry_points=["invenio_base.blueprints"],
        extension_entry_points=["invenio_base.apps"],
        converter_entry_points=["invenio_base.converters"],
        instance_path=os.getenv("INVENIO_INSTANCE_PATH"),
        static_folder=os.getenv("INVENIO_INSTANCE_PATH") + "/static",
        root_path=os.getenv("INVENIO_INSTANCE_PATH"),
        wsgi_factory=wsgi_proxyfix(create_wsgi_factory({"/api": factory.create_api})),
        static_url_path="/static",
        app_class=factory.app_class(),
    )

    return create_app_e2e


@pytest.fixture(scope="module")
def create_app(create_app_e2e):
    """Flask app fixture."""
    return create_app_e2e
