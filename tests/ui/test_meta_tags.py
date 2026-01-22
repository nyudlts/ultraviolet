# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Tests for meta.html."""

from flask import url_for
from invenio_access.permissions import system_identity
from invenio_accounts.testutils import login_user_via_session
from invenio_rdm_records.proxies import current_rdm_records_service


def test_meta_tags(full_record, services, client, app, db, admin_user):
    """Test that verifies all meta tags appear in the record"""

    service = current_rdm_records_service
    data = full_record.copy()
    draft = service.create(system_identity, data)
    db.session.commit()
    draft = service.read_draft(system_identity, draft.id)
    record = service.publish(system_identity, draft.id)
    recid = record["id"]
    with app.test_request_context():
        record_url = url_for('invenio_app_rdm_records.record_detail', pid_value=recid)

    login_user_via_session(client, email=admin_user.email)

    response = client.get(record_url)
    html_content = response.data.decode()

    assert '<meta name="citation_title" content="InvenioRDM" />' in html_content, "Missing citation_title tag"
    assert '<meta name="description" content="A description with HTML tags" />' in html_content, "Missing description tag"
    assert '<meta name="citation_author" content="Nielsen, Lars Holm" />' in html_content, "Missing author tag"
    assert '<meta name="citation_publication_date" content="2020/09/01" />' in html_content, "Missing citation_publication_date tag"
    assert '<meta name="citation_publisher" content="InvenioRDM" />' in html_content, "Missing citation_publisher tag"
    assert '<meta name="citation_doi" content="10.1234/inveniordm.1234" />' in html_content, "Missing citation_doi tag"
    assert '<meta name="citation_keywords" content="custom" />' in html_content, "Missing citation_keywords tag"
    assert '<meta name="citation_abstract_html_url" content="https://127.0.0.1:5000/records/' in html_content, "Missing citation_abstract_html_url tag"
    assert '<meta name="citation_contributor" content="Nielsen, Lars Holm" />' in html_content, "Missing contirbutor tag"
