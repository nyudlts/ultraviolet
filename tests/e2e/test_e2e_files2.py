import pytest
from invenio_communities.proxies import current_communities
import json

@pytest.fixture()
def myuser(UserFixture, app, db):
    u = UserFixture(
        email="adminUV1@test.com",
        password="adminUV",
    )
    u.create(app, db)
    return u

@pytest.fixture()
def service():
    return current_communities.service

@pytest.fixture()
def location(db):
    """Create a default location for testing."""
    from invenio_files_rest.models import Location
    location = Location(name='pytest-location', uri='/tmp/pytest-location', default=True)
    db.session.add(location)
    db.session.commit()
    return location

def create_community_data(name, description, type, visibility, policy):
    data_to_use = {
        "access": {
            "visibility": visibility,
            "member_policy": policy,
            "record_policy": policy,
        },
        "slug": ('-'.join(name.split())).lower(),
        "metadata": {
            "title": name,
            "description": description,
            "type": {
                "id": type
            },
        },
    }
    return json.loads(json.dumps(data_to_use))

def test_create_community(db, service, myuser, location, app):
    # Print the DB connection string for debugging
    print(app.config["SQLALCHEMY_DATABASE_URI"])  # This will print the connection string

    # Create community data
    community_data = create_community_data(
        'MyCommunity', 'This is an example Community.', 'organization', 'public', 'open'
    )
    
    # Create a community using the service and myuser's identity
    community = service.create(data=community_data, identity=myuser.identity)
    
    # Assertions
    assert community["metadata"]["type"]["id"] == "organization"
