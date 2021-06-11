"""E2E test of the front page."""

from flask import url_for

def test_frontpage(live_server, browser):
    """Test retrieval of front page."""
    browser.get(url_for('invenio_app_rdm.index', _external=True))
    html = browser.page_source
    print(html)
    assert (
            "UltraViolet"
            == browser.find_element_by_tag_name("h1")
            .text
    )
