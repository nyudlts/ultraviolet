"""Tests for the permission helpers in ultraviolet.policies."""

from uuid import UUID

import pytest
from flask_principal import Identity, RoleNeed
from invenio_communities.generators import CommunityRoleNeed

from ultraviolet.policies import has_community_role

COMMUNITY_ID = "12345678-9012-3456-7890-123456789012"
OTHER_COMMUNITY_ID = "98765432-1098-7654-3210-987654321098"


def identity_with(*needs):
    identity = Identity(1)
    identity.provides.update(needs)
    return identity


def test_has_community_role():
    identity = identity_with(
        RoleNeed("depositor"), CommunityRoleNeed(COMMUNITY_ID, "depositor")
    )

    assert has_community_role(identity, "depositor")
    assert not has_community_role(identity, "curator")
    # a global role of the same name is not a community role
    assert not has_community_role(identity_with(RoleNeed("depositor")), "depositor")


@pytest.mark.parametrize(
    "community_id, expected",
    [
        pytest.param(COMMUNITY_ID, True, id="that community"),
        pytest.param(UUID(COMMUNITY_ID), True, id="community id as UUID"),
        pytest.param(OTHER_COMMUNITY_ID, False, id="another community"),
    ],
)
def test_has_community_role_in_a_given_community(community_id, expected):
    identity = identity_with(CommunityRoleNeed(COMMUNITY_ID, "depositor"))

    assert has_community_role(identity, "depositor", community_id) == expected
