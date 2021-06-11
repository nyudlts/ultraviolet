from _pytest import monkeypatch
from invenio_app.factory import create_app

def test_var_assigned(monkeypatch):
    """Mocking setting configuration using environment varuables """
    monkeypatch.setenv('APP_ALLOWED_HOSTS', ['ultraviolet.dlib.nyu.edu'])
    monkeypatch.setenv('SQLALCHEMY_DATABASE_URI', 'postgresql+psycopg2://test:test@somehost.com/test')
    monkeypatch.setenv('RDM_RECORDS_DOI_DATACITE_ENABLED', True)
    monkeypatch.setenv('RDM_RECORDS_DOI_DATACITE_USERNAME', 'doimockuser')
    monkeypatch.setenv('RDM_RECORDS_DOI_DATACITE_PASSWORD', 'doimockpassword')
    monkeypatch.setenv('RDM_RECORDS_DOI_DATACITE_PREFIX', 'mock.prefix')
    monkeypatch.setenv('RDM_RECORDS_DOI_DATACITE_TEST_MODE', True)
    monkeypatch.setenv('SITE_UI_URL', 'ultraviolet.dlib.nyu.edu')
    monkeypatch.setenv('SITE_API_URL', 'ultraviolet.dlib.nyu.edu/api')
    app = create_app()
    assert app.config.get("APP_ALLOWED_HOSTS") == "['ultraviolet.dlib.nyu.edu']"
    assert app.config.get("SQLALCHEMY_DATABASE_URI") == "postgresql+psycopg2://test:test@somehost.com/test"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_ENABLED") == "True"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_USERNAME") == "doimockuser"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_PASSWORD") == "doimockpassword"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_PREFIX") == "mock.prefix"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_TEST_MODE") == "True"
    assert app.config.get("SITE_UI_URL") == "ultraviolet.dlib.nyu.edu"
    assert app.config.get("SITE_API_URL") == "ultraviolet.dlib.nyu.edu/api"


def test_var_noassigned():
    """Mocking using default configuration """
    app = create_app()
    assert app.config.get("APP_ALLOWED_HOSTS") == ['0.0.0.0', 'localhost', '127.0.0.1']
    assert app.config.get("SQLALCHEMY_DATABASE_URI") == "postgresql+psycopg2://nyu-data-repository:nyu-data-repository@localhost/nyu-data-repository"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_ENABLED") == "False"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_USERNAME") == "..."
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_PASSWORD") == "..."
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_PREFIX") == "10.1234"
    assert app.config.get("RDM_RECORDS_DOI_DATACITE_TEST_MODE") == "True"
    assert app.config.get("SITE_UI_URL") == "https://127.0.0.1:5000"
    assert app.config.get("SITE_API_URL") == "https://127.0.0.1:5000/api"
