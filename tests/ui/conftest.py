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


from invenio_app.factory import create_app as create_ui
import pytest


@pytest.fixture(scope="module")
def create_app():
    """Flask app fixture."""
    return create_ui