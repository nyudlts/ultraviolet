from flask_login import current_user
from flask_principal import RoleNeed
from invenio_access.permissions import authenticated_user, superuser_access, system_identity
from invenio_records_permissions.generators import Generator
from invenio_search.engine import dsl



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


class Depositor(Generator):
    """Allows users with the "depositor" role."""

    def __init__(self):
        """Constructor."""
        super(Depositor, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        return [RoleNeed("depositor")]


class Viewer(Generator):
    """Allow NYU Viewers for files restricted to NYU"""

    def __init__(self):
        """Constructor."""
        super(Viewer, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        return [RoleNeed("viewer")]


class Curator(Generator):
    """Allow Curator"""

    def __init__(self):
        """Constructor."""
        super(Curator, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        return [RoleNeed("curator")]
