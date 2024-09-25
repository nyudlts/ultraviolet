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
    return app_config


# overriding instance path allows us to make sure we use ultraviolet templates
@pytest.fixture(scope="module")
def ultraviolet_instance_path():
    return os.path.join(sys.prefix, "var", "instance")
