# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Test account pages elements: Change Password (removed), Developer Applications of Applications (removed)."""

from flask import url_for
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session

def test_change_password_not_in_profile_form(services, client, app, admin_user):
    """Test that verifies Change Password field is not present in the profile form."""
    
    uploads_url = url_for("invenio_userprofiles.profile", _external=True) 
    login_user_via_session(client, email=admin_user.email)
    response = client.get(uploads_url)
    html = response.data.decode()
    
    assert admin_user.email in response.data.decode()
    assert "Profile" in response.data.decode(), "'Profile' field should appear in html, but is not."
    assert "Change password" not in response.data.decode(), "'Change password' field should not appear in html."


def test_developer_applications_not_in_applications_page(services, client, app, admin_user):
    """Test that verifies Developer Applications field is not present in the applications page."""
    
    uploads_url = url_for("invenio_oauth2server_settings.index", _external=True) 
    login_user_via_session(client, email=admin_user.email)
    response = client.get(uploads_url)
    html = response.data.decode()
    
    assert admin_user.email in response.data.decode()
    assert "Applications" in response.data.decode(), "'Profile' field should appear in html, but is not."
    assert "Developer Applications" not in response.data.decode(), "'Developer Applications' field should not appear in html."

