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
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import multiprocessing

"""This is needed so live_server fixture can be used on Mac with python3.8 
    https://github.com/pytest-dev/pytest-flask/issues/104 """
multiprocessing.set_start_method("fork")


def test_frontpage(chrome_driver):
    """Test retrieval of front page."""
    try:
        browser = chrome_driver
        browser.get("https://127.0.0.1:5000/")
        assert "Search UltraViolet" == browser.find_element(By.TAG_NAME, "h1").text
    except Exception as e:
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
            browser.save_screenshot(f'screenshots/test_frontpage_failure_{".".join(random.choices(string.ascii_lowercase + string.digits, k=10))}.png')
        raise e