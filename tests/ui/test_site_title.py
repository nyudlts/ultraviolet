# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Test for title of search.html."""

from flask import url_for

def test_search_page_title(client, app):
    """Test that the search page includes our new title text."""
    with app.test_request_context():
        search_url = url_for('invenio_search_ui.search')

    response = client.get(search_url)
    assert response.status_code == 200

    html_content = response.data.decode()
    assert "<title>Search Results | UltraViolet | NYU Libraries</title>" in html_content
