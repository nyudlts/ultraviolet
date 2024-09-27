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


from io import BytesIO
from invenio_access.permissions import system_identity


def test_one_small_file(service, minimal_record, client_admin):
    """Restricted record fixture."""
    data = minimal_record.copy()
    data["files"]["enabled"] = True
    data["access"]["record"] = "restricted"
    data["access"]["files"] = "restricted"

    # Create
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

    record_view = client_admin.get("/records/" + record['id']).data
    # Download all button should present
    assert "Download all" in record_view.decode("utf-8")
    # Downlaod button should present
    expected_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/test.pdf?download=1">'.format(record['id'])
    assert expected_button_html in record_view.decode("utf-8")

def test_one_large_file(service, minimal_record, client_admin):
    """Restricted record fixture."""
    data = minimal_record.copy()
    data["files"]["enabled"] = True
    data["access"]["record"] = "restricted"
    data["access"]["files"] = "restricted"

    # Create
    draft = service.create(system_identity, data)

    # Add a file
    service.draft_files.init_files(
        system_identity, draft.id, data=[{"key": "test.pdf"}]
    )

    # larger than config limit
    service.draft_files.set_file_content(
        system_identity, draft.id, "test.pdf", BytesIO(b'1' * (10**6))
    )
    service.draft_files.commit_file(system_identity, draft.id, "test.pdf")

    # Publish
    record = service.publish(system_identity, draft.id)

    record_view = client_admin.get("/records/" + record['id']).data
    # Download all button should not present
    assert "Download all" not in record_view.decode("utf-8")
    # Downlaod button should not present
    expected_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/test.pdf?download=1">'.format(record['id'])
    assert expected_button_html not in record_view.decode("utf-8")
    
def test_two_files(service, minimal_record, client_admin):
    """Restricted record fixture."""
    data = minimal_record.copy()
    data["files"]["enabled"] = True
    data["access"]["record"] = "restricted"
    data["access"]["files"] = "restricted"

    # Create
    draft = service.create(system_identity, data)

    # Add two files
    service.draft_files.init_files(
        system_identity, draft.id, data=[{"key": "small.pdf"}, {"key": "large.pdf"}]
    )
    
    service.draft_files.set_file_content(
        system_identity, draft.id, "small.pdf", BytesIO(b"test file")
    )
    service.draft_files.commit_file(system_identity, draft.id, "small.pdf")
    # larger than config limit
    service.draft_files.set_file_content(
        system_identity, draft.id, "large.pdf", BytesIO(b'1' * (10**6))
    )
    service.draft_files.commit_file(system_identity, draft.id, "large.pdf")

    # Publish
    record = service.publish(system_identity, draft.id)

    record_view = client_admin.get("/records/" + record['id']).data
    print(record_view)
    # Download all button show not present
    assert "Download all" not in record_view.decode("utf-8")
    # Download button for small file should present
    small_file_download_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/small.pdf?download=1">'.format(record['id'])
    assert small_file_download_button_html in record_view.decode("utf-8")
    # Download button for large file should not present
    large_file_download_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/large.pdf?download=1">'.format(record['id'])
    assert large_file_download_button_html not in record_view.decode("utf-8")