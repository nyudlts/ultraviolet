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
def create_app(ultraviolet_instance_path):
    """Flask app fixture."""
    create_app_e2e = factory.create_app_factory(
        "invenio",
        config_loader=create_config_loader(config=None, env_prefix="Invenio"),
        blueprint_entry_points=["invenio_base.blueprints"],
        extension_entry_points=["invenio_base.apps"],
        converter_entry_points=["invenio_base.converters"],
        instance_path=ultraviolet_instance_path,
        static_folder=os.path.join(ultraviolet_instance_path, "static"),
        root_path=ultraviolet_instance_path,
        wsgi_factory=wsgi_proxyfix(create_wsgi_factory({"/api": factory.create_api})),
        static_url_path="/static",
        app_class=factory.app_class(),
    )
    return create_app_e2e

@pytest.fixture(scope="module", autouse=True)
def update_invenio_config():
    config_file_path = os.path.join(os.path.dirname(__file__), '../../invenio.cfg')
    with open(config_file_path, 'r') as file:
        original_lines = file.readlines()
    updated_lines = original_lines.copy()

    key1 = 'MAX_FILE_SIZE'
    value1 = '10 * 1024 * 1024'  # Set to 10 MB
    key2 = 'DATACITE_ENABLED'
    value2 = 'False'

    for i, line in enumerate(updated_lines):
        if line.startswith(key1):
            updated_lines[i] = f"{key1} = {value1}\n"
        if line.startswith(key2):
            updated_lines[i] = f"{key2} = {value2}\n"

    with open(config_file_path, 'w') as file:
        file.writelines(updated_lines)

    yield

    with open(config_file_path, 'w') as file:
        file.writelines(original_lines)
