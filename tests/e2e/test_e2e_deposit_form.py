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


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
@pytest.fixture(scope="module")
def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    # chrome_options.add_argument('--headless=new')
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
        pass
        # driver.quit()




"""This is needed so live_server fixture can be used on Mac with python3.8"""
# multiprocessing.set_start_method("fork")


# @pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes', reason="Skipping E2E tests because E2E environment variable is not set")
# def test_element_not_in_deposit_form1(app, live_server, chrome_driver,
#                               resource_type_v,
#                               subject_v,
#                               languages_v,
#                               affiliations_v,
#                               title_type_v,
#                               description_type_v,
#                               date_type_v,
#                               contributors_role_v,
#                               relation_type_v,
#                               licenses_v,
#                               funders_v,
#                               awards_v,
#                               creatorsroles_v):
#     """Test for hidding References field on deposit form """
    
#     email = "TEST@test.org"
#     password = "123456"

#     # Setup user and permissions
#     with app.app_context():
#         user = testutils.create_test_user(email, password, active=True)
#         datastore = app.extensions["security"].datastore
        
#         admin_role = datastore.create_role(name="administration-access")
#         action_role = ActionRoles.create(action=administration_access_action, role=admin_role)
#         datastore.db.session.add(action_role)
#         _, role = datastore._prepare_role_modify_args(user, "administration-access")
#         datastore.add_role_to_user(user, role)
#         datastore.commit()

#     base_url = url_for("invenio_app_rdm.index", _external=True)
#     login_url = f"{base_url}login/"
#     chrome_driver.get(login_url)

#     chrome_driver.find_element(By.NAME, "email").send_keys(email)
#     chrome_driver.find_element(By.NAME, "password").send_keys(password)
    
#     submit_button = WebDriverWait(chrome_driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
#     )
#     submit_button.click()

#     dashboard_url = f"{base_url}me/uploads"
#     chrome_driver.get(dashboard_url)

#     new_upload_button = WebDriverWait(chrome_driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui.tiny.button.positive.left.labeled.icon[href='/uploads/new']"))
#     )
#     new_upload_button.click()

#     page_source = chrome_driver.page_source
#     # Assert that the text "References" is not present in the HTML
#     assert "Reference string" not in page_source, "'References' field is present in the HTML, but it should not be."



@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes', reason="Skipping E2E tests because E2E environment variable is not set")
def test_element_not_in_deposit_form2(app, live_server, chrome_driver,
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
                              admin_user):
    """Test for hidding References field on deposit form """

    base_url = url_for("invenio_app_rdm.index", _external=True)
    login_url = f"{base_url}login/"
    chrome_driver.get(login_url)

    chrome_driver.find_element(By.NAME, "email").send_keys(admin_user.email)
    chrome_driver.find_element(By.NAME, "password").send_keys(admin_user.password)
    
    submit_button = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
    )
    submit_button.click()

    dashboard_url = f"{base_url}me/uploads"
    chrome_driver.get(dashboard_url)

    new_upload_button = WebDriverWait(chrome_driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui.tiny.button.positive.left.labeled.icon[href='/uploads/new']"))
    )
    new_upload_button.click()

    page_source = chrome_driver.page_source
    # Assert that the text "References" is not present in the HTML
    assert "Reference string" not in page_source, "'References' field is present in the HTML, but it should not be."