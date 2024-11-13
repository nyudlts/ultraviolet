from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_access.permissions import system_identity
from io import BytesIO
from flask import url_for

from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session

def test_element_not_in_deposit_form(minimal_record, services, client,  app, db, register_file_service, admin_user):
    """Test that verifies References field is not present in the deposit form."""
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

    # larger than config limit
    service.draft_files.set_file_content(
        system_identity, draft.id, "test.pdf", BytesIO(b'1' * (10**6))
    )
    service.draft_files.commit_file(system_identity, draft.id, "test.pdf")
    with app.test_request_context():
        draft_url = url_for('invenio_app_rdm_records.deposit_edit', pid_value=draft.id)
    
    login_user(admin_user, remember=True)
    login_user_via_session(client, email=admin_user.email)

    response = client.get(draft_url)
    
    assert 'references' not in response.data.decode()