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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

@pytest.fixture(scope="module")
def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.page_load_strategy = 'none'
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        yield driver
    finally:
        driver.quit()