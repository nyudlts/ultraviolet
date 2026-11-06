from flask import current_app
from flask_principal import Permission, RoleNeed
from invenio_access import Permission as InvenioPermission
from invenio_access.permissions import system_process
from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_rdm_records.services import RDMRecordPermissionPolicy
from invenio_rdm_records.services.generators import (
    IfAtLeastOneCommunity,
    SecretLinks,
    RecordCommunitiesAction,
    RecordOwners,
    AccessGrant,
    IfRestricted,
    ResourceAccessToken,
)
from invenio_records_permissions.generators import (
    SystemProcess,
    AuthenticatedUser,
    AnyUser,
    Disable,
)

from .generators import AdminSuperUser, Depositor, Curator, Viewer
from invenio_records_resources.services.files.generators import IfTransferType
from invenio_records_resources.services.files.transfer import LOCAL_TRANSFER_TYPE


SITE_DEPOSIT_ROLES = ("depositor", "viewer")
"""Site-wide roles that can already create records (see ``can_manage``)."""


def has_community_role(identity, role, community_id=None):
    """Whether the identity holds ``role`` in a community.

    Any community when ``community_id`` is not given.
    """
    return any(
        getattr(need, "method", None) == "community"
        and getattr(need, "role", None) == role
        and (community_id is None or str(need.value) == str(community_id))
        for need in identity.provides
    )


def has_site_deposit_access(identity):
    """Whether the identity can create records regardless of any community.

    ``InvenioPermission`` always includes superusers and expands the needs
    granted to users and roles in the database.
    """
    return InvenioPermission(
        system_process, *(RoleNeed(role) for role in SITE_DEPOSIT_ROLES)
    ).allows(identity)


def community_depositor_may_create(action, identity):
    """Whether being a depositor in any community allows ``action``.

    Creating a record has no community context, so the check cannot be
    expressed with a generator.
    """
    return action == "create" and has_community_role(identity, "depositor")


def may_submit_record(action, identity, community_id, site_access):
    """Whether ``action`` is allowed by the rule limiting who submits records.

    Only ``submit_record`` is limited: users who can create records only
    through the community "depositor" role may submit to the communities they
    are a depositor of, and no others. ``site_access`` is a callable taking
    the identity, so that it only runs when the cheap check is not enough.
    """
    if action != "submit_record":
        return True
    return (
        community_id is not None
        and has_community_role(identity, "depositor", community_id)
    ) or site_access(identity)


class UltraVioletPermissionPolicy(RDMRecordPermissionPolicy):
    """Access control configuration for records.

    Note that even if the array is empty, the invenio_access Permission class
    always adds the ``superuser-access``, so admins will always be allowed.
    """

    NEED_LABEL_TO_ACTION = {
        "bucket-update": "update_files",
        "bucket-read": "read_files",
        "object-read": "read_files",
    }

    #
    # High-level permissions (used by low-level)
    #
    can_manage = [
        RecordOwners(),
        Viewer(),
        SystemProcess(),
        AccessGrant("manage"),
        AdminSuperUser(),
        Depositor(),
        RecordCommunitiesAction("manage"),
    ]
    can_curate = can_manage + [
        SecretLinks("edit"),
        AccessGrant("edit"),
        Curator(),
        RecordCommunitiesAction("curate"),
    ]
    can_preview = can_manage + [SecretLinks("preview"), AccessGrant("view"), Curator()]
    can_view = can_manage + [
        SecretLinks("view"),
        AccessGrant("view"),
        RecordCommunitiesAction("view"),
        Viewer(),
    ]

    can_authenticated = [AuthenticatedUser(), SystemProcess()]
    can_all = [AnyUser(), SystemProcess()]

    #
    #  Records
    #
    # Allow submitting new record
    can_create = can_manage
    # Allow reading metadata of a record
    can_read = [
        IfRestricted("record", then_=can_view, else_=can_all),
    ]
    can_read_files = [
        IfRestricted("files", then_=can_view, else_=can_all),
        ResourceAccessToken("read"),
    ]
    # Need to repeat here to make sure custom can_read_files will be used for local transfer type
    can_get_content_files = [
        IfTransferType(LOCAL_TRANSFER_TYPE, can_read_files),
        SystemProcess(),
    ]

    #
    # Drafts
    #
    # Allow ability to search drafts
    can_search_drafts = can_authenticated
    # Allow reading metadata of a draft
    can_read_draft = can_preview
    # Allow reading files of a draft
    can_draft_read_files = can_preview
    # Allow downloading files of a draft (only for local transfer type)
    # needed to repeat here to make sure custom can_draft_read_files will be used together with
    # base policy. This is done not to delete existing options. Probably need to fix it later.
    can_draft_get_content_files = [
        IfTransferType(
            LOCAL_TRANSFER_TYPE,
            can_draft_read_files + RDMRecordPermissionPolicy.can_draft_read_files,
        ),
        SystemProcess(),
    ]

    # Allow updating metadata of a draft
    can_update_draft = can_curate
    # Allow uploading, updating and deleting files in drafts
    can_draft_create_files = can_curate
    can_draft_update_files = can_curate
    can_draft_delete_files = can_curate

    #
    # PIDs
    #
    can_pid_reserve = can_curate
    can_pid_delete = can_curate

    #
    # Actions
    #
    # Allow to put a record in edit mode (create a draft from record)
    can_edit = can_curate
    # Allow deleting/discarding a draft and all associated files
    can_delete_draft = can_curate
    # Allow creating a new version of an existing published record.
    can_new_version = can_curate
    # Allow publishing a new record or changes to an existing record.
    # Outside of a community, owning the draft is not enough: that would let
    # community depositors (who can create records without the site-wide
    # depositor role) publish without going through a community.
    can_publish = [
        IfAtLeastOneCommunity(
            then_=can_curate,
            else_=[g for g in can_curate if not isinstance(g, RecordOwners)],
        ),
    ]
    # Allow lifting a record or draft.
    can_lift_embargo = can_manage
    # Allow deleting of records by admins
    can_delete = can_manage
    can_delete_files = can_manage

    #
    # Disabled actions (these should not be used or changed)
    #
    can_update = [Disable()]
    can_create_files = [Disable()]
    can_update_files = [Disable()]

    def allows(self, identity):
        """Also let community depositors create records."""
        return super().allows(identity) or community_depositor_may_create(
            self.action, identity
        )


class UltraVioletCommunityPermissionPolicy(CommunityPermissionPolicy):
    """Community permissions, confining community depositors to their community."""

    def allows(self, identity):
        """Limit who can submit records to a community."""
        return super().allows(identity) and may_submit_record(
            self.action,
            identity,
            self.over.get("community_id"),
            has_site_deposit_access,
        )


def ultraviolet_admin_permission_factory(_admin_view):
    return Permission(RoleNeed(current_app.config["ADMIN_ROLE"]))
