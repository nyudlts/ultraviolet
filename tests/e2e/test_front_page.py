"""E2E test of the front page."""

from flask import url_for
from selenium.webdriver.common.by import By

def test_frontpage(live_server, browser):
    """Test retrieval of front page."""
    browser.get(url_for('invenio_app_rdm.index', _external=True))
    assert (
            "UltraViolet"
            == browser.find_element(By.TAG_NAME, 'h1')
            .text
    )
