"""Tests for what community depositors can do with records.

``UltraVioletPermissionPolicy.allows`` only asks the generator-based policy and
applies ``community_depositor_may_create``; the generator-based check needs a
full application, so it is covered by the E2E tests. Everything else is tested
here.
"""

from types import SimpleNamespace

import pytest
from flask_principal import Identity
from invenio_communities.generators import CommunityRoleNeed
from invenio_rdm_records.services.generators import RecordOwners
from invenio_records_permissions.generators import SystemProcess

from ultraviolet.generators import AdminSuperUser, Curator, Depositor, Viewer
from ultraviolet.policies import (
    UltraVioletPermissionPolicy,
    community_depositor_may_create,
)

COMMUNITY_ID = "12345678-9012-3456-7890-123456789012"
OTHER_COMMUNITY_ID = "98765432-1098-7654-3210-987654321098"


def identity_with(*needs):
    identity = Identity(1)
    identity.provides.update(needs)
    return identity


def publish_generators(*community_ids):
    """Types of the generators that decide who can publish such a record."""
    communities = SimpleNamespace(ids=set(community_ids))
    record = SimpleNamespace(parent=SimpleNamespace(communities=communities))
    (conditional,) = UltraVioletPermissionPolicy.can_publish
    return {type(g) for g in conditional._generators(record)}


#
# Creating records
#
@pytest.mark.parametrize(
    "needs, allowed",
    [
        pytest.param(
            [CommunityRoleNeed(COMMUNITY_ID, "depositor")], True, id="depositor"
        ),
        pytest.param(
            [CommunityRoleNeed(OTHER_COMMUNITY_ID, "depositor")],
            True,
            id="depositor of any community",
        ),
        *(
            pytest.param([CommunityRoleNeed(COMMUNITY_ID, role)], False, id=role)
            for role in ("reader", "curator", "manager", "owner")
        ),
        pytest.param([], False, id="no roles"),
    ],
)
def test_only_community_depositors_can_create(needs, allowed):
    assert community_depositor_may_create("create", identity_with(*needs)) == allowed


@pytest.mark.parametrize(
    "action", ["delete", "lift_embargo", "manage", "delete_files", "publish"]
)
def test_community_depositor_is_only_granted_create(action):
    identity = identity_with(CommunityRoleNeed(COMMUNITY_ID, "depositor"))

    assert not community_depositor_may_create(action, identity)


#
# Publishing records
#
def test_publishing_outside_a_community_only_drops_the_owner():
    inside = publish_generators(COMMUNITY_ID)
    outside = publish_generators()

    assert inside - outside == {RecordOwners}
    assert outside <= inside


def test_site_roles_can_still_publish_outside_a_community():
    # global depositors, curators, viewers and admins are unchanged
    assert {Depositor, Curator, Viewer, AdminSuperUser, SystemProcess} <= (
        publish_generators()
    )
