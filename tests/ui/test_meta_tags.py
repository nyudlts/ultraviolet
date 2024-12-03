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


from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_access.permissions import system_identity
from io import BytesIO
from flask import url_for

from invenio_accounts.testutils import login_user_via_session

def test_meta_tags(full_record, services, client, app, db, admin_user):
    """Test that verifies all meta tags appear in the record"""

    app.config["DATACITE_PREFIX"] = "10.1234"
    app.config["DATACITE_ENABLED"] = "true"

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

    assert '<meta name="citation_title"' in html_content, "Missing citation_title tag"
    assert '<meta name="description"' in html_content, "Missing description tag"
    assert '<meta name="citation_author"' in html_content, "Missing author tag"
    assert '<meta name="citation_publication_date"' in html_content, "Missing citation_publication_date tag"
    assert '<meta name="citation_publisher"' in html_content, "Missing citation_publisher tag"
    assert '<meta name="citation_doi"' in html_content, "Missing citation_doi tag"
    assert '<meta name="citation_keywords"' in html_content, "Missing citation_keywords tag"
    assert '<meta name="citation_abstract_html_url"' in html_content, "Missing citation_abstract_html_url tag"
