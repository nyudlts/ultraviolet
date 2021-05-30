import os
from unittest import mock
from invenio_app.factory import create_app

@mock.patch.dict(os.environ, {"APP_ALLOWED_HOSTS": "ultraviolet.dlib.nyu.edu"})
def test_var():
    app=create_app()
    apple = app.config.get("APP_ALLOWED_HOSTS")
    assert apple == "ultraviolet.dlib.nyu.edu"
