"""Tests for the community roles defined in invenio.cfg."""

import runpy
from pathlib import Path

import pytest
from invenio_communities.config import COMMUNITIES_ROLES as DEFAULT_ROLES
from invenio_communities.roles import RoleRegistry

INVENIO_CFG = Path(__file__).parents[2] / "invenio.cfg"


@pytest.fixture(scope="module")
def uv_config():
    """The configuration defined in invenio.cfg."""
    return runpy.run_path(str(INVENIO_CFG))


@pytest.fixture()
def roles(uv_config):
    """The configured community roles."""
    return RoleRegistry(uv_config["COMMUNITIES_ROLES"])


def test_depositor_role_is_defined(roles):
    assert "depositor" in roles
    depositor = roles["depositor"]
    assert str(depositor.title) == "Depositor"
    # no curation or management rights: uploads are reviewed by curators
    assert not depositor.can_curate
    assert not depositor.can_manage
    assert not depositor.is_owner


def test_managers_and_owners_can_assign_depositor(roles):
    assert roles["manager"].can_manage_role("depositor")
    assert roles["owner"].can_manage_role("depositor")
    assert not roles["curator"].can_manage_role("depositor")
    assert not roles["reader"].can_manage_role("depositor")


def test_default_roles_are_unchanged(roles):
    for default in DEFAULT_ROLES:
        role = roles[default["name"]]
        for key, value in default.items():
            if key == "can_manage_roles":
                assert role.can_manage_roles[: len(value)] == value
            else:
                assert getattr(role, key) == value
