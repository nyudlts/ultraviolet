import pytest
from invenio_access.permissions import system_identity
from invenio_communities.proxies import current_communities

from ultraviolet.cli import ultraviolet
from ultraviolet.tasks import enable_subcommunities_for

SLUG = "parent-community"


@pytest.fixture()
def parent(running_app, search_clear):
    community = current_communities.service.create(
        system_identity,
        {
            "slug": SLUG,
            "metadata": {"title": "Parent Community"},
            "access": {"visibility": "public"},
        },
    )
    current_communities.service.indexer.refresh()
    return community


@pytest.fixture()
def child(parent):
    enable_subcommunities_for(SLUG)
    community = current_communities.service.create(
        system_identity,
        {
            "slug": "child-community",
            "metadata": {"title": "Child Community"},
            "access": {"visibility": "public"},
            "parent": {"id": str(parent.id)},
        },
    )
    current_communities.service.indexer.refresh()
    return community


def subcommunities_allowed(community_id):
    return current_communities.service.record_cls.pid.resolve(
        community_id
    ).children.allow


def test_enables_subcommunities(parent, capsys):
    assert not subcommunities_allowed(parent.id)

    enable_subcommunities_for(SLUG)

    assert subcommunities_allowed(parent.id)
    assert "now enabled" in capsys.readouterr().out


def test_updates_the_search_index(parent):
    enable_subcommunities_for(SLUG)
    current_communities.service.indexer.refresh()

    read = current_communities.service.read(system_identity, parent.id)
    assert read.data["children"]["allow"] is True


def test_can_be_run_twice(parent, capsys):
    enable_subcommunities_for(SLUG)
    capsys.readouterr()

    enable_subcommunities_for(SLUG)

    assert subcommunities_allowed(parent.id)
    assert "already enabled" in capsys.readouterr().out


def test_unknown_community(running_app, capsys):
    enable_subcommunities_for("no-such-community")

    assert "does not exist" in capsys.readouterr().out


def test_command_enables_subcommunities(running_app, parent):
    runner = running_app.app.test_cli_runner()
    result = runner.invoke(ultraviolet, ["enable-subcommunities", SLUG])

    assert result.exit_code == 0, result.output
    assert "now enabled" in result.output
    assert subcommunities_allowed(parent.id)


def test_a_subcommunity_cannot_have_subcommunities(child, capsys):
    capsys.readouterr()

    enable_subcommunities_for("child-community")

    assert not subcommunities_allowed(child.id)
    out = capsys.readouterr().out
    assert "is a subcommunity of '{}'".format(SLUG) in out
    assert "now enabled" not in out
