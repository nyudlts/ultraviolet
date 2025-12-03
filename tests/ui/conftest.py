# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
# conftest.py
"""Pytest configuration."""

import pytest
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.proxies import current_service_registry


@pytest.fixture()
def services(running_app, search_clear):
    """RDM Record Service."""
    return running_app.app.extensions["invenio-rdm-records"].records_service


@pytest.fixture(scope="function")
def register_file_service(app):
    """Register RDMFileService in the service registry."""
    # Get the existing draft_files service instance
    existing_service = current_rdm_records_service.draft_files
    # Register the existing service instance
    current_service_registry.register(existing_service, "rdm-files")
    return existing_service
