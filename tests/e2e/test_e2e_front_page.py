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

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import multiprocessing
import pytest

"""This is needed so live_server fixture can be used on Mac with python3.8 
    https://github.com/pytest-dev/pytest-flask/issues/104 """
multiprocessing.set_start_method("fork")

@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes', reason="Skipping E2E tests because E2E environment variable is not set")
def test_frontpage(live_server, browser):
    """Test retrieval of front page."""
    browser.get(url_for("invenio_app_rdm.index", _external=True))
    assert "Search Ultraviolet Data Repository 22" == browser.find_element(By.TAG_NAME, "h1").text
