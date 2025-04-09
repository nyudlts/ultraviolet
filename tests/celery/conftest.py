
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
# conftest.py
"""Pytest configuration for customized celery tasks."""

import pytest
from invenio_rdm_records.services.pids import providers
from fake_datacite_client import FakeDataCiteClient


@pytest.fixture()
def services(running_app, search_clear):
    """RDM Record Service."""
    return running_app.app.extensions["invenio-rdm-records"].records_service

# refer to invenio record rdm package on master branch
# tests/services/pids/test_pids_tasks.py
@pytest.fixture(scope="module")
def mock_datacite_client():
    """Mock DataCite client."""
    return FakeDataCiteClient

@pytest.fixture(scope='module')
def celery_config_ext(celery_config_ext):
    celery_config_ext['CELERY_TASK_ALWAYS_EAGER'] = True
    return celery_config_ext

# modify application configuration
@pytest.fixture(scope="module")
def app_config(app_config, mock_datacite_client, celery_config_ext):
    # sqllite refused to create mock db without those parameters and they are missing
    app_config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": False,
        "pool_recycle": 3600,
    }
    # need this to make sure separate indexes are created for testing
    app_config["SEARCH_INDEX_PREFIX"] = "q"
    app_config["SERVER_NAME"] = "127.0.0.1"
    app_config["MAX_FILE_SIZE"] = 50
    app_config["REST_CSRF_ENABLED"] = False
    app_config["APP_DEFAULT_SECURE_HEADERS"] = {
        'content_security_policy': {
            'default-src': [
                "'self'",
                'data:',  # for fonts
                "'unsafe-inline'",  # for inline scripts and styles
                "blob:",  # for pdf preview
                # Add your own policies here (e.g. analytics)
            ],
        },
        'content_security_policy_report_only': False,
        'content_security_policy_report_uri': None,
        'force_file_save': False,
        'force_https': False,
        'force_https_permanent': False,
        'frame_options': 'sameorigin',
        'frame_options_allow_from': None,
        'session_cookie_http_only': True,
        'session_cookie_secure': True,
        'strict_transport_security': True,
        'strict_transport_security_include_subdomains': True,
        'strict_transport_security_max_age': 31556926,  # One year in seconds
        'strict_transport_security_preload': False,
    }

    # for doi tests
    app_config["DATACITE_ENABLED"] = True
    app_config["DATACITE_USERNAME"] = "fake"
    app_config["DATACITE_PASSWORD"] = "fake"
    app_config["DATACITE_PREFIX"] = "10.9999"
    app_config["DATACITE_TEST_MODE"] = True

    app_config["RDM_PERSISTENT_IDENTIFIER_PROVIDERS"] = [
        providers.DataCitePIDProvider(
            "datacite",
            client=mock_datacite_client("datacite", config_prefix="DATACITE"),
            label="DOI",
        ),
        providers.ExternalPIDProvider(
            "external",
            "doi",
            validators=[providers.BlockedPrefixes(config_names=["DATACITE_PREFIX"])],
            label="DOI (external)",
        ),
        providers.OAIPIDProvider(
            "oai",
            label="OAI ID"
        )
    ]
    return app_config
