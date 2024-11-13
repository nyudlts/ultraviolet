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
from invenio_rdm_records.proxies import current_rdm_records_service


def test_one_small_file(minimal_record, client_with_login, services, app, db, register_file_service):
    """
    Test files page for small file in the application.
    The Download button, Download all button, and file name download link should present.
    """
    
    service = current_rdm_records_service
    
    data = minimal_record.copy()
    data["files"]["enabled"] = True

    # Create draft
    draft = service.create(system_identity, data)
    db.session.commit()
    draft = service.read_draft(system_identity, draft.id)
    
    # Add a file
    service.draft_files.init_files(
        system_identity, draft.id, data=[{"key": "test.pdf"}]
    )
    service.draft_files.set_file_content(
        system_identity, draft.id, "test.pdf", BytesIO(b"test file")
    )
    
    service.draft_files.commit_file(system_identity, draft.id, "test.pdf")

    record = service.publish(system_identity, draft.id)
    record_view = client_with_login.get("/records/" + record['id']).data
    html = record_view.decode("utf-8")


    # Download all button should present
    assert "Download all" in html
    # Downlaod button should present
    expected_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/test.pdf?download=1">'.format(record['id'])
    assert expected_button_html in html
    # File name download link should present
    expected_namelink_html = '<a class="wrap-long-link" href="/records/{}/files/test.pdf?download=1">test.pdf</a>'.format(record['id'])
    assert expected_namelink_html in html



def test_one_large_file(minimal_record, client_with_login, services, app, db):
    """
    This test verifies files page for large file in the application.
    The Download button, Download all button, and file name download link should not present.
    """

    service = current_rdm_records_service

    data = minimal_record.copy()
    data["files"]["enabled"] = True

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
    record_view = client_with_login.get("/records/" + record['id']).data
    html = record_view.decode("utf-8")
    
    # Download all button should not present
    assert "Download all" not in html
    # Downlaod button should not present
    expected_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/test.pdf?download=1">'.format(record['id'])
    assert expected_button_html not in html
    # File name download link should not present
    expected_namelink_html = '<a class="wrap-long-link" href="/records/{}/files/test.pdf?download=1">test.pdf</a>'.format(record['id'])
    assert expected_namelink_html not in html


def test_two_files(minimal_record, client_with_login, services, app, db):
    """
    This test verifies files page for a small file and a large file in the application.
    The Download all buton should not present.
    The Download button and file name download link should present for small file.
    The Download all button, Download button, and file name download link should not present for large file.
    """

    service = current_rdm_records_service
    
    data = minimal_record.copy()
    data["files"]["enabled"] = True

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
    record_view = client_with_login.get("/records/" + record['id']).data
    html = record_view.decode("utf-8")
    
    # Download all button show not present
    assert "Download all" not in html

    # Download button for small file should present
    small_file_download_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/small.pdf?download=1">'.format(record['id'])
    assert small_file_download_button_html in html
    # File name download link should present
    expected_namelink_html = '<a class="wrap-long-link" href="/records/{}/files/small.pdf?download=1">small.pdf</a>'.format(record['id'])
    assert expected_namelink_html in html

    # Download button for large file should not present
    large_file_download_button_html = '<a role="button" class="ui compact mini button" href="/records/{}/files/large.pdf?download=1">'.format(record['id'])
    assert large_file_download_button_html not in html
    # File name download link should not present
    expected_namelink_html = '<a class="wrap-long-link" href="/records/{}/files/large.pdf?download=1">large.pdf</a>'.format(record['id'])
    assert expected_namelink_html not in html