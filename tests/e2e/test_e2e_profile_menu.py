# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""View tests of the front page."""

import os
import time

import pytest
from flask import url_for
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access
from invenio_accounts import testutils
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes',
                    reason="Skipping E2E tests because E2E environment variable is not set")
def test_admins_see_administration_item(app, live_server, browser):
    """Test for Profile menu Administration entry"""
    email = "foobar@test.org"
    password = "123456"

    with app.app_context():
        user = testutils.create_test_user(email, password, active=True)
        datastore = app.extensions["security"].datastore

        admin_role = datastore.create_role(name="administration-access")
        action_role = ActionRoles.create(action=superuser_access, role=admin_role)
        datastore.db.session.add(action_role)
        _, role = datastore._prepare_role_modify_args(user, "administration-access")
        datastore.add_role_to_user(user, role)
        datastore.commit()

    browser.set_window_size(1920, 3980)
    browser.get(url_for("invenio_app_rdm.index", _external=True))
    browser.find_element(By.LINK_TEXT, "Log in").click()
    browser.find_element(By.NAME, "email").send_keys(email)
    browser.find_element(By.NAME, "password").send_keys(password)
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
    )
    submit_button.click()
    time.sleep(2)
    page_source = browser.page_source

    assert "Search UltraViolet" in page_source
    assert "Administration" in page_source


@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes',
                    reason="Skipping E2E tests because E2E environment variable is not set")
def test_regular_users_do_not_see_administration_item(app, live_server, browser):
    """Test for Profile menu Administration entry"""
    email = "foobarbaz@test.org"
    password = "123456"

    with app.app_context():
        testutils.create_test_user(email, password, active=True)

    browser.set_window_size(1920, 3980)
    browser.get(url_for("invenio_app_rdm.index", _external=True))
    browser.find_element(By.LINK_TEXT, "Log in").click()
    browser.find_element(By.NAME, "email").send_keys(email)
    browser.find_element(By.NAME, "password").send_keys(password)
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
    )
    submit_button.click()
    time.sleep(2)
    page_source = browser.page_source

    assert "Search UltraViolet" in page_source
    assert "Administration" not in page_source
