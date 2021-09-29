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

def test_view1(base_client):
    # Depends on 'base_app' fixture
    front_view = base_client.get('/').data
    assert "NYU Scholarly Communication and Information Policy" in front_view.decode("utf-8")
