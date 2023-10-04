# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""View tests of the deposit form."""
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session

def test_deposit (  client, users, db, admin_user, prepare_indexes):
    user = users["user1"]
    login_user(user, remember=True)
    login_user_via_session(client, email=user.email)
    front_view = client.get("/uploads/new?community=opendata").data
    assert "opendata" in front_view.decode("utf-8")
