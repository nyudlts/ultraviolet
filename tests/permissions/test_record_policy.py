"""Tests for record creation by community depositors.

The parent policy check is stubbed: evaluating it needs a full application
(Redis and a database). These tests cover only the rule added by
``UltraVioletPermissionPolicy.allows``.
"""

from types import SimpleNamespace

import pytest
from flask_principal import Identity, RoleNeed
from invenio_communities.generators import CommunityRoleNeed
from invenio_rdm_records.services.generators import RecordOwners
from invenio_records_permissions.generators import SystemProcess
from invenio_records_permissions.policies.base import BasePermissionPolicy

from ultraviolet.generators import AdminSuperUser, Curator, Depositor, Viewer
from ultraviolet.policies import UltraVioletPermissionPolicy, has_community_role

COMMUNITY_ID = "c441b9c2-40e0-4035-96cc-8e13bd28d0f7"


def identity_with(*needs):
    identity = Identity(1)
    identity.provides.update(needs)
    return identity


@pytest.fixture()
def parent_allows(monkeypatch):
    """Set what the generator-based policy check answers."""
    answer = {"value": False}
    monkeypatch.setattr(
        BasePermissionPolicy,
        "allows",
        lambda self, identity: answer["value"],
        raising=False,
    )
    return answer


def can(action, identity):
    return UltraVioletPermissionPolicy(action).allows(identity)


def test_has_community_role():
    identity = identity_with(
        RoleNeed("depositor"), CommunityRoleNeed(COMMUNITY_ID, "depositor")
    )

    assert has_community_role(identity, "depositor")
    assert not has_community_role(identity, "curator")
    # a global role of the same name is not a community role
    assert not has_community_role(identity_with(RoleNeed("depositor")), "depositor")


def test_community_depositor_can_create(parent_allows):
    identity = identity_with(CommunityRoleNeed(COMMUNITY_ID, "depositor"))

    assert can("create", identity)


def test_community_depositor_in_any_community_can_create(parent_allows):
    other_community = "11111111-2222-3333-4444-555555555555"

    assert can("create", identity_with(CommunityRoleNeed(other_community, "depositor")))


def test_parent_policy_still_decides_for_everyone_else(parent_allows):
    parent_allows["value"] = True

    assert can("create", identity_with())
    assert can("delete", identity_with())


@pytest.mark.parametrize("role", ["reader", "curator", "manager", "owner"])
def test_other_community_roles_cannot_create(parent_allows, role):
    assert not can("create", identity_with(CommunityRoleNeed(COMMUNITY_ID, role)))


def test_user_without_roles_cannot_create(parent_allows):
    assert not can("create", identity_with())


@pytest.mark.parametrize(
    "action", ["delete", "lift_embargo", "manage", "delete_files", "publish"]
)
def test_community_depositor_is_only_granted_create(parent_allows, action):
    identity = identity_with(CommunityRoleNeed(COMMUNITY_ID, "depositor"))

    assert not can(action, identity)


def record_in_communities(*community_ids):
    communities = SimpleNamespace(ids=set(community_ids))
    return SimpleNamespace(parent=SimpleNamespace(communities=communities))


def publish_generators(record):
    """The generators that decide who can publish the given record."""
    (conditional,) = UltraVioletPermissionPolicy.can_publish
    return conditional._generators(record)


def types(generators):
    return {type(g) for g in generators}


def test_owner_can_publish_a_record_in_a_community():
    generators = publish_generators(record_in_communities(COMMUNITY_ID))

    assert RecordOwners in types(generators)


def test_owner_cannot_publish_a_record_outside_a_community():
    generators = publish_generators(record_in_communities())

    assert RecordOwners not in types(generators)


def test_site_roles_can_still_publish_outside_a_community():
    generators = publish_generators(record_in_communities())

    # global depositors, curators, viewers and admins are unchanged
    assert {Depositor, Curator, Viewer, AdminSuperUser, SystemProcess} <= types(
        generators
    )


def test_publish_outside_a_community_only_drops_the_owner():
    inside = publish_generators(record_in_communities(COMMUNITY_ID))
    outside = publish_generators(record_in_communities())

    assert types(inside) - types(outside) == {RecordOwners}
    assert types(outside) <= types(inside)
