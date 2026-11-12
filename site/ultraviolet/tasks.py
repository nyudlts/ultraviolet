"""Site tasks that can be used from the command line or ``invenio shell``."""

from invenio_db import db
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records_resources.proxies import current_service_registry


def enable_subcommunities_for(parent_slug):
    """Allow the community with slug ``parent_slug`` to have subcommunities."""
    community_service = current_service_registry.get("communities")

    try:
        parent = community_service.record_cls.pid.resolve(parent_slug)
    except PIDDoesNotExistError:
        print("Community with slug '{}' does not exist".format(parent_slug))
        return

    if parent.parent is not None:
        print(
            "Community with slug '{}' is a subcommunity of '{}' and "
            "subcommunities can't have subcommunities of their own".format(
                parent_slug, parent.parent.slug
            )
        )
        return

    if parent.children.allow:
        print(
            "Subcommunities are already enabled for community with slug '{}'".format(
                parent_slug
            )
        )
        print(
            "To create a subcommunity, head to /communities/{}/subcommunities/new".format(
                parent_slug
            )
        )
        return

    parent.children.allow = True
    parent.commit()
    db.session.commit()
    community_service.indexer.index_by_id(parent.id)

    print(
        "Subcommunities are now enabled for community with slug '{}'".format(
            parent_slug
        )
    )
    print(
        "To create a subcommunity, head to /communities/{}/subcommunities/new".format(
            parent_slug
        )
    )
