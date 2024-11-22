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

from invenio_app.factory import create_app as create_ui_api
import pytest


@pytest.fixture(scope="module")
def create_app(app_config):
    """Create test app."""
    return create_ui_api

@pytest.fixture()
def services(running_app, search_clear):
    """RDM Record Service."""
    return running_app.app.extensions["invenio-rdm-records"].records_service
