# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""E2E test of Communities"""

import os
import time

import pytest
from flask import url_for
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access
from invenio_accounts import testutils
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes',
                    reason="Skipping E2E tests because E2E environment variable is not set")
def test_user_cannot_create_community(app, live_server,
                                      resource_type_v,
                                      subject_v,
                                      languages_v,
                                      affiliations_v,
                                      title_type_v,
                                      description_type_v,
                                      date_type_v,
                                      contributors_role_v,
                                      relation_type_v,
                                      licenses_v,
                                      funders_v,
                                      awards_v,
                                      creatorsroles_v,
                                      browser):
    email = "TEST@test.org"
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

    time.sleep(5)
    browser.set_window_size(1920, 3980)

    # Log in
    browser.get(url_for("invenio_app_rdm_records.deposit_create", _external=True))
    browser.find_element(By.NAME, "email").send_keys(email)
    browser.find_element(By.NAME, "password").send_keys(password)
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
    )

    submit_button.click()

    browser.get(url_for("invenio_communities.communities_frontpage", _external=True))

    # Ensure "Communities" link in header is removed
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.CSS_SELECTOR, 'a[href="/communities"]')

    # Ensure "New community" link is disabled
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.CSS_SELECTOR, 'a[href="/communities/new"]')
