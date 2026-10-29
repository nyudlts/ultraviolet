import pytest
from flask_principal import Identity, RoleNeed, UserNeed
from invenio_access.permissions import any_user, authenticated_user, system_identity
from invenio_communities.generators import CommunityRoleNeed
from invenio_communities.proxies import current_communities
from invenio_rdm_records.proxies import (
    current_rdm_records_service,
    current_record_communities_service,
)


def person(user_id=None, roles=(), community_roles=()):
    identity = Identity(user_id)
    identity.provides.add(any_user)
    if user_id is not None:
        identity.provides.add(UserNeed(user_id))
        identity.provides.add(authenticated_user)
    for role in roles:
        identity.provides.add(RoleNeed(role))
    for community_id, role in community_roles:
        identity.provides.add(CommunityRoleNeed(community_id, role))
    return identity


def create_community(slug):
    community = current_communities.service.create(
        system_identity,
        {
            "slug": slug,
            "metadata": {"title": slug},
            "access": {"visibility": "public"},
        },
    )
    return str(community.id)


@pytest.fixture()
def anonymous_visitor():
    return person()


@pytest.fixture()
def logged_in_user(users):
    return person(users["user5"].id)


@pytest.fixture()
def record_owner(users):
    return person(users["user2"].id)


@pytest.fixture()
def depositor(users):
    return person(users["user5"].id, roles=["depositor"])


@pytest.fixture()
def curator(users):
    return person(users["user5"].id, roles=["curator"])


@pytest.fixture()
def viewer(users):
    return person(users["user5"].id, roles=["viewer"])


@pytest.fixture()
def superuser(superuser_identity):
    return superuser_identity


@pytest.fixture()
def records(running_app, search_clear, minimal_record, users):
    owner = person(users["user2"].id, roles=["depositor"])
    service = current_rdm_records_service

    def published(visibility):
        data = dict(minimal_record)
        data["access"] = {"record": visibility, "files": visibility}
        draft = service.create(owner, data)
        record = service.publish(system_identity, draft.id)
        return service.record_cls.pid.resolve(record.id)

    draft = service.create(owner, dict(minimal_record))
    return {
        "in general": None,
        "public record": published("public"),
        "restricted record": published("restricted"),
        "draft": service.draft_cls.pid.resolve(draft.id, registered_only=False),
    }


@pytest.fixture()
def community_id(running_app, search_clear):
    return create_community("members-community")


@pytest.fixture()
def another_community_id(running_app, search_clear):
    return create_community("other-community")


@pytest.fixture()
def community_reader(users, community_id):
    return person(users["user5"].id, community_roles=[(community_id, "reader")])


@pytest.fixture()
def community_curator(users, community_id):
    return person(users["user5"].id, community_roles=[(community_id, "curator")])


@pytest.fixture()
def community_manager(users, community_id):
    return person(users["user5"].id, community_roles=[(community_id, "manager")])


@pytest.fixture()
def community_owner(users, community_id):
    return person(users["user5"].id, community_roles=[(community_id, "owner")])


@pytest.fixture()
def member_of_another_community(users, another_community_id):
    return person(users["user5"].id, community_roles=[(another_community_id, "owner")])


@pytest.fixture()
def community_records(records, community_id, users):
    owner = person(users["user2"].id, roles=["depositor"])
    service = current_rdm_records_service

    for group in ("public record", "restricted record"):
        _, errors = current_record_communities_service.add(
            system_identity,
            records[group].pid.pid_value,
            {"communities": [{"id": community_id}]},
        )
        assert not errors

    draft = service.edit(owner, records["public record"].pid.pid_value)
    return {
        "in general": None,
        "public record": service.record_cls.pid.resolve(
            records["public record"].pid.pid_value
        ),
        "restricted record": service.record_cls.pid.resolve(
            records["restricted record"].pid.pid_value
        ),
        "draft": service.draft_cls.pid.resolve(draft.id, registered_only=False),
    }
