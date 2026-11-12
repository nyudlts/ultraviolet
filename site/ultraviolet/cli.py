"""UltraViolet commands for the ``invenio`` command line."""

import click
from flask.cli import with_appcontext

from . import tasks


@click.group()
def ultraviolet():
    """UltraViolet site commands."""


@ultraviolet.command("enable-subcommunities")
@click.argument("parent-slug")
@with_appcontext
def enable_subcommunities(parent_slug):
    """Allow the community with slug PARENT_SLUG to have subcommunities."""
    tasks.enable_subcommunities_for(parent_slug)
