from flask_login import current_user
from flask_principal import RoleNeed
from invenio_access.permissions import authenticated_user, superuser_access
from invenio_records_permissions.generators import Generator
from invenio_search.engine import dsl


def get_roles(record, user_role):
    return current_user.roles


class AdminSuperUser(Generator):
    """Allows admin superusers"""

    def __init__(self):
        """Constructor."""
        super(AdminSuperUser, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [superuser_access]

    def query_filter(self, identity=None, **kwargs):
        """Filters for current identity as super user."""
        if superuser_access in identity.provides:
            return dsl.Q('match_all')
        else:
            return []


class Curator(Generator):
    """Allow Curator"""

    def __init__(self):
        """Constructor."""
        super(Curator, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        return [RoleNeed("curator")]


class Depositor(Generator):
    """Allows users with the "depositor" role."""

    def __init__(self):
        """Constructor."""
        super(Depositor, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        return [RoleNeed("depositor")]


class ProprietaryRecordPermissions(Generator):
    """ProprietaryRecordPermissions

    Allows users who were granted  a specific role to view additional records
    Main use case are records which should be only available to NYU community
    Another use case are records that only can be accessed by users who met special conditions.
    In second case record curators check the condition outside Ultraviolet and then assign the
    user to a special role.
    InvenioRDM data model does not allow to add role to the access section of the record ( See https://inveniordm.docs.cern.ch/reference/metadata/)
    As a proof of concept solution we use additional_descriptions field where value will be equal to "role" and type will be equal
    to "Technical Info". Hopefully InvenioRDM will modify their data model and we won't have to use this model in production
    We expect that even users who do not have access to the records will be able to see them in the search so query filter is set to any_user
    """

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        if record is None:
            # 'record is None' means that this must be a 'create'
            # this should be allowed for any authenticated user
            return [authenticated_user]

        additional_descriptions = record.get("metadata").get("additional_descriptions", [])
        for index, description in enumerate(additional_descriptions, start=0):
            if description.get("type") == "technical-info":
                role = description.get("description")
                if "<p>" in role:
                    role = role.replace("<p>", "")

                if "</p>" in role:
                    role = role.replace("</p>", "")
                return [RoleNeed(role.name)]
        return []

    def query_filter(self, **kwargs):
        """Match all in search."""
        return dsl.Q('can_all')


class PublicViewer(Generator):
    """Allow Public Viewer for any files that are open"""

    def __init__(self):
        """Constructor."""
        super(PublicViewer, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        roles = get_roles(record, "public_viewer")
        if len(roles) == 0:
            return []
        return [RoleNeed(role) for role in roles]
