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


def test_front_page(db,base_client):
    # Depends on 'base_app' fixture
    front_view = base_client.get("/").data
    assert (
        "https://library.nyu.edu/departments/scholarly-communications-information-policy/"
        in front_view.decode("utf-8")
    )
    assert (
        "NYU Scholarly Communication and Information Policy"
        in front_view.decode("utf-8")
    )


def test_header_menu_button(db,base_client):
    front_view = base_client.get("/").data
    assert "Browse" in front_view.decode("utf-8")
    assert "FAQs" in front_view.decode("utf-8")
    assert "Deposit" in front_view.decode("utf-8")
