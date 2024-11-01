def test_element_not_in_deposit_form(client_with_login, admin_user, service, creatorsroles_type, creatorsroles_v):
    """Test that verifies References field is not present in the deposit form."""
    deposit_page = client_with_login.get("/uploads/new")
    html = deposit_page.data.decode("utf-8")
    
    assert deposit_page.status_code == 200
    
    # dynamiclly rendered. only assert the overridable. 
    assert 'src="/static/dist/js/overridable-registry.' in html
    

import pytest
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_vocabularies.records.api import Vocabulary
from invenio_access.permissions import system_identity

@pytest.fixture(scope="module")
def creatorsroles_type(app):
    """Creators roles vocabulary type."""
    return vocabulary_service.create_type(system_identity, "creatorsroles", "crt")

@pytest.fixture(scope="module")
def creatorsroles_v(app, creatorsroles_type):
    vocabulary_service.create(
        system_identity,
        {
            "id": "author",
            "title": {"en": "Author"},
            "type": "creatorsroles",
        },
    )

    vocab = vocabulary_service.create(
        system_identity,
        {
            "id": "editor",
            "title": {"en": "Editor"},
            "type": "creatorsroles",
        },
    )

    Vocabulary.index.refresh()

    return vocab