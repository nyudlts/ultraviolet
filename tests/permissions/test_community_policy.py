"""Tests for the rule limiting who can submit records to a community.

``UltraVioletCommunityPermissionPolicy.allows`` only asks the default policy
and applies ``may_submit_record``; the default policy needs a full application,
so it is covered by the E2E tests. Everything else is tested here.
"""

from uuid import UUID

import pytest
from flask_principal import Identity
from invenio_communities.generators import CommunityRoleNeed

from ultraviolet.policies import may_submit_record

COMMUNITY_ID = "12345678-9012-3456-7890-123456789012"
OTHER_COMMUNITY_ID = "98765432-1098-7654-3210-987654321098"


def community_role(role="depositor", community_id=COMMUNITY_ID):
    return CommunityRoleNeed(community_id, role)


def identity_with(*needs):
    identity = Identity(1)
    identity.provides.update(needs)
    return identity


def can_submit(identity, community_id=COMMUNITY_ID, site_access=False):
    return may_submit_record(
        "submit_record", identity, community_id, lambda identity: site_access
    )


@pytest.mark.parametrize(
    "needs, community_id, allowed",
    [
        pytest.param([community_role()], COMMUNITY_ID, True, id="depositor there"),
        pytest.param(
            [community_role()], UUID(COMMUNITY_ID), True, id="community id as UUID"
        ),
        pytest.param(
            [community_role()], OTHER_COMMUNITY_ID, False, id="depositor elsewhere"
        ),
        *(
            pytest.param([community_role(role)], COMMUNITY_ID, False, id=role)
            for role in ("reader", "curator", "manager", "owner")
        ),
        pytest.param([], COMMUNITY_ID, False, id="no roles"),
        pytest.param([community_role()], None, False, id="missing community id"),
    ],
)
def test_submitting_needs_the_depositor_role_in_that_community(
    needs, community_id, allowed
):
    assert can_submit(identity_with(*needs), community_id) == allowed


def test_site_access_allows_submitting_anywhere():
    assert can_submit(identity_with(), OTHER_COMMUNITY_ID, site_access=True)
    assert can_submit(identity_with(), None, site_access=True)


def test_site_access_is_not_checked_for_depositors_of_that_community():
    # it may need the database, so only check it when it can change the answer
    def site_access(identity):
        raise AssertionError("site access should not be checked")

    assert may_submit_record(
        "submit_record", identity_with(community_role()), COMMUNITY_ID, site_access
    )


@pytest.mark.parametrize("action", ["read", "update", "members_add", "search"])
def test_other_actions_are_unchanged(action):
    assert may_submit_record(action, identity_with(), COMMUNITY_ID, lambda _: False)
