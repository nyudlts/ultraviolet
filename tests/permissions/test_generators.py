from io import BytesIO

import pytest
from flask_principal import RoleNeed
from invenio_access import superuser_access
from ultraviolet.generators import AdminSuperUser, Depositor, Curator, Viewer


def test_admin_superuser():
    generator = AdminSuperUser()

    assert generator.needs() == [superuser_access]


def test_depositor():
    generator = Depositor()
    assert generator.needs() == [RoleNeed("depositor")]


def test_viewer():
    generator = Viewer()
    assert generator.needs() == [RoleNeed("viewer")]


def test_curator():
    generator = Curator()
    assert generator.needs() == [RoleNeed("curator")]
