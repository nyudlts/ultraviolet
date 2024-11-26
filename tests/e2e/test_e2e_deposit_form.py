# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""View tests of the front page."""



import os
import time
import pytest

from flask import url_for
from invenio_access.models import ActionRoles
from invenio_accounts import testutils
from invenio_access.models import ActionUsers
from invenio_access.permissions import superuser_access
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# # create user on the fly - can login
@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes', reason="Skipping E2E tests because E2E environment variable is not set")
def test_element_not_in_deposit_form1(app, live_server,
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
    """Test for hidding References field on deposit form """
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
    browser.get(url_for("invenio_app_rdm_records.deposit_create", _external=True))
    browser.find_element(By.NAME, "email").send_keys(email)
    browser.find_element(By.NAME, "password").send_keys(password)
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
    )
    submit_button.click()
    page_source = browser.page_source
    # Assert that the text "References" is not present in the HTML
    assert "Reference string" not in page_source, "'References' field is present in the HTML, but it should not be."
