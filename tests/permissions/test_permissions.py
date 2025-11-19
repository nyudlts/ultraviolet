# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet Permssions is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

def test_user_without_special_role(base_client, UserFixture, app, db, create_proprietary_record):
    client = base_client
    user = UserFixture(
        email="test@test1.org",
        password="superuser",
    )
    user.create(app, db)
    recid = create_proprietary_record(client)
    url = f"/records/{recid}"

    # Anonymous user can't list files
    response = client.get(url, headers=headers)
    assert 403 == response.status_code

def test_anonymous(base_client, app, db, create_proprietary_record):
    client = base_client
    recid = create_proprietary_record(client)
    url = f"/records/{recid}"

    # Anonymous user can't list files
    response = client.get(url, headers=headers)
    assert 403 == response.status_code

def test_user_with_special_role(base_client, UserFixture, app, db, create_proprietary_record):
    client = base_client
    user = UserFixture(
        email="test@test1.org",
        password="superuser",
    )
    user.create(app, db)
    role = create_roles(['nyu'])
    assign_roles(user, [role])
    login_user(client, user)

    recid = create_proprietary_record["recid"]

    url = f"/records/{recid}"

    # Anonymous user can't list files
    response = client.get(url, headers=headers)
    assert 200 == response.status_code