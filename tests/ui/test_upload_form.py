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

def test_deposit( _search_create_indexes, app_config, base_client, users, admin_user, db, opendata_community, resource_type_item, language_item, subject_item,
                   creator_role_item, contributor_role_item, title_type_item,description_type_item, date_type_item,
                   relations_type_item):
    user = users["user1"]
    login_user(user, remember=True)
    login_user_via_session(base_client, email=user.email)
    front_view = base_client.get("/uploads/new?community=opendata").data
    assert "opendata" in front_view.decode("utf-8")
