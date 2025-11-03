# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""View tests of the front page."""


from flask import url_for
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session

def test_reference_not_in_deposit_form(services, client, app, admin_user):
    """Test that verifies References field is not present in the deposit form."""
    
    uploads_url = url_for("invenio_app_rdm_records.deposit_create", _external=True) 
    login_user_via_session(client, email=admin_user.email)
    response = client.get(uploads_url)
    assert admin_user.email in response.data.decode()
    assert "Reference string" not in response.data.decode(), "'References' field is present in the HTML, but it should not be."

