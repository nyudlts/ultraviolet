# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""View tests of the front page."""
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session


def test_community(base_client,users,admin_user,db):
    user = users["user1"]
    login_user(user, remember=True)
    login_user_via_session(base_client, email=user.email)
    front_view = base_client.get("/me/uploads/new").data
    assert "communities" in front_view.decode("utf-8")