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
"""Pytest configuration."""


import invenio_app.factory as factory
from invenio_base.wsgi import wsgi_proxyfix
from invenio_config import create_config_loader
import pytest
import os
from invenio_app.factory import create_ui


@pytest.fixture()
def service(running_app, search_clear):
    """RDM Record Service."""
    return running_app.app.extensions["invenio-rdm-records"].records_service
