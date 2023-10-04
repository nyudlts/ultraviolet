# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""E2E test of the front page."""

from flask import url_for
from selenium.webdriver.common.by import By
import multiprocessing
from time import sleep
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session


"""This is needed so live_server fixture can be used on Mac with python3.8 
    https://github.com/pytest-dev/pytest-flask/issues/104 """
multiprocessing.set_start_method("fork")

def test_frontpage(live_server, browser):
    """Test retrieval of front page."""
    browser.get(url_for("invenio_app_rdm.index", _external=True))
    assert "Search Ultraviolet" == browser.find_element(By.TAG_NAME, "h1").text

def test_deposit_form(live_server, browser,owner,opendata_community,db):
    """Test default community in deposit form"""
    browser.get(url_for("security.login", _external=True))
    login_form = browser.find_element_by_name("login_user_form")
    login_form.find_element_by_name("email").send_keys(owner.email)
    login_form.find_element_by_name("password").send_keys(owner.password)
    login_form.submit()
    sleep(1)
    browser.get(url_for("invenio_app_rdm_users.uploads", _external=True))
    assert "opendata" in browser.find_element(By.LINK_TEXT, "New upload").get_attribute("href")
    upload_button = browser.find_element(By.LINK_TEXT, "New upload")
    upload_button.click()
    assert  "uploads/new?community=opendata" in browser.current_url