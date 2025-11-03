# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Tests for restricted file message on record page."""


from io import BytesIO
from invenio_access.permissions import system_identity
from invenio_rdm_records.proxies import current_rdm_records_service


def test_restricted_file_message(minimal_record, services, app, db, register_file_service, client):
    """
    Test restricted file message on record page.
    """
    
    service = current_rdm_records_service

    data = minimal_record.copy()
    data["files"]["enabled"] = True

    data["access"]["record"] = "public"
    data["access"]["files"] = "restricted"

    # Create a record with a restricted file
    draft = service.create(system_identity, data)

    # Add a file
    service.draft_files.init_files(
        system_identity, draft.id, data=[{"key": "test.pdf"}]
    )
    service.draft_files.set_file_content(
        system_identity, draft.id, "test.pdf", BytesIO(b"test file")
    )
    service.draft_files.commit_file(system_identity, draft.id, "test.pdf")

    # Publish
    record = service.publish(system_identity, draft.id)
    record_view = client.get("/records/" + record['id']).data
    html = record_view.decode("utf-8")
    print(html)

    # Restricted file message should present
    assert "The files associated with this metadata record are restricted to members of the NYU community." in html
