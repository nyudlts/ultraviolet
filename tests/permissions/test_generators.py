from io import BytesIO

import pytest
from flask_principal import RoleNeed
from invenio_access import superuser_access
from invenio_files_rest.models import Bucket, Location, ObjectVersion
from ultraviolet.generators import AdminSuperUser, Depositor, PublicViewer, Curator, IfSuppressedFile, \
    RestrictedDataUser, Viewer


def test_admin_superuser():
    generator = AdminSuperUser()

    assert generator.needs() == [superuser_access]

@pytest.mark.parametrize("user_role", ["depositor"], indirect=True)
def test_depositor(user_roles_propriatery_record, propriatery_record):
    generator = Depositor()
    assert generator.needs() == [RoleNeed("depositor")]


@pytest.mark.skip(reason="Failing due to get_roles")
@pytest.mark.parametrize("user_role", ["viewer"], indirect=True, )
def test_viewer(user_roles_propriatery_record, propriatery_record):
    generator = Viewer()
    record = user_roles_propriatery_record

    assert generator.needs(record) == [RoleNeed("viewer")]


@pytest.mark.skip(reason="Failing due to get_roles")
@pytest.mark.parametrize("user_role", ["restricted_data_user"], indirect=True)
def test_restricted_data_user(user_roles_propriatery_record, propriatery_record):
    generator = RestrictedDataUser()
    record = user_roles_propriatery_record

    assert generator.needs(record) == [RoleNeed("restricted_data_user")]


@pytest.mark.skip(reason="Failing due to get_roles")
@pytest.mark.parametrize("user_role", ["public_viewer"], indirect=True)
def test_public_viewer(user_roles_propriatery_record, propriatery_record):
    generator = PublicViewer()
    record = user_roles_propriatery_record

    assert generator.needs(record) == [RoleNeed("public_viewer")]


@pytest.mark.parametrize("user_role", ["curator"], indirect=True)
def test_curator(user_roles_propriatery_record, propriatery_record):
    generator = Curator()
    record = user_roles_propriatery_record

    assert generator.needs(record) == [RoleNeed("curator")]



def test_suppressed(db, bucket_from_dir, create_real_record, location):
    l1 = Location(name="suppressed", uri="file:///tmp", default=False)
    l2 = Location(name="public", uri="file:///tmp", default=True)
    db.session.add(l1)
    db.session.add(l2)

    generator = IfSuppressedFile(RoleNeed("admin"), RoleNeed("any_user"))

    suppressed_location = Location.get_by_name("suppressed")

    assert suppressed_location

    suppressed_bucket = Bucket.create(suppressed_location)
    ObjectVersion.create(
        suppressed_bucket, key="suppressed.txt", stream=BytesIO(b"suppressed")
    )
    record = create_real_record(bucket=suppressed_bucket)

    assert generator._condition(record) == True

    bucket = Bucket.create(location)
    ObjectVersion.create(bucket, key="public.txt", stream=BytesIO(b"public"))
    record = create_real_record(bucket=bucket)

    assert generator._condition(record) == False