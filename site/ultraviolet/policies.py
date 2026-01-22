from flask import current_app
from flask_principal import Permission, RoleNeed
from invenio_rdm_records.services import RDMRecordPermissionPolicy
from invenio_rdm_records.services.generators import SecretLinks, RecordCommunitiesAction, RecordOwners, AccessGrant, IfRestricted, ResourceAccessToken
from invenio_records_permissions.generators import SystemProcess, AuthenticatedUser, AnyUser, Disable

from .generators import AdminSuperUser, Depositor, Curator, Viewer


class UltraVioletPermissionPolicy(RDMRecordPermissionPolicy):
    """Access control configuration for records.

    Note that even if the array is empty, the invenio_access Permission class
    always adds the ``superuser-access``, so admins will always be allowed.
    """

    NEED_LABEL_TO_ACTION = {
        'bucket-update': 'update_files',
        'bucket-read': 'read_files',
        'object-read': 'read_files',
    }

    #
    # High-level permissions (used by low-level)
    #
    can_manage = [ RecordOwners(),Viewer(), SystemProcess(), AccessGrant("manage"), AdminSuperUser(), Depositor(), RecordCommunitiesAction("manage")]
    can_curate = can_manage + [SecretLinks("edit"), AccessGrant("edit"),Curator(),RecordCommunitiesAction("curate")]
    can_preview = can_manage + [SecretLinks("preview"), AccessGrant("view"),Curator()]
    can_view = can_manage + [SecretLinks("view"),AccessGrant("view"), RecordCommunitiesAction("view"), Viewer()]

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

    #
    # Drafts
    #
    # Allow ability to search drafts
    can_search_drafts = can_authenticated
    # Allow reading metadata of a draft
    can_read_draft = can_preview
    # Allow reading files of a draft
    can_draft_read_files = can_preview
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
    can_publish = can_curate
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


def ultraviolet_admin_permission_factory(_admin_view):
    return Permission(RoleNeed(current_app.config["ADMIN_ROLE"]))
