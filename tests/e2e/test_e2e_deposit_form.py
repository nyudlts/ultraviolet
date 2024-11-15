import multiprocessing
import os

import pytest
from flask import url_for
from invenio_access.models import ActionRoles
from invenio_accounts import testutils
from invenio_administration.permissions import administration_access_action
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""This is needed so live_server fixture can be used on Mac with python3.8"""
# multiprocessing.set_start_method("fork")


@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes', reason="Skipping E2E tests because E2E environment variable is not set")
def test_element_not_in_deposit_form(app, live_server, browser,
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
                              creatorsroles_v):
    """Test for hidding References field on deposit form """
    
    email = "TEST@test.org"
    password = "123456"

    # Setup user and permissions
    with app.app_context():
        user = testutils.create_test_user(email, password, active=True)
        datastore = app.extensions["security"].datastore
        
        admin_role = datastore.create_role(name="administration-access")
        action_role = ActionRoles.create(action=administration_access_action, role=admin_role)
        datastore.db.session.add(action_role)
        _, role = datastore._prepare_role_modify_args(user, "administration-access")
        datastore.add_role_to_user(user, role)
        datastore.commit()

    base_url = url_for("invenio_app_rdm.index", _external=True)
    login_url = f"{base_url}login/"
    browser.get(login_url)

    browser.find_element(By.NAME, "email").send_keys(email)
    browser.find_element(By.NAME, "password").send_keys(password)
    
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
    )
    submit_button.click()

    dashboard_url = f"{base_url}me/uploads"
    browser.get(dashboard_url)

    new_upload_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui.tiny.button.positive.left.labeled.icon[href='/uploads/new']"))
    )
    new_upload_button.click()

    page_source = browser.page_source
    print(page_source)
    # Assert that the text "References" is not present in the HTML
    assert "Reference string" not in page_source, "'References' field is present in the HTML, but it should not be."
