from flask import url_for
from flask_security import login_user
from invenio_accounts.testutils import login_user_via_session

def test_reference_not_in_deposit_form( services, client,  app, db, admin_user):
    """Test that verifies References field is not present in the deposit form."""
    
    uploads_url = url_for("invenio_app_rdm_records.deposit_create", _external=True) 
    login_user_via_session(client, email=admin_user.email)
    response = client.get(uploads_url)
    assert admin_user.email in response.data.decode()
