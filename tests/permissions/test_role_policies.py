from permission_checks import allowed, denied


def test_anonymous_visitor_can(anonymous_visitor, records):
    can = {
        "public record": {"read", "read_files"},
    }

    assert allowed(anonymous_visitor, records, can) == can


def test_anonymous_visitor_cannot(anonymous_visitor, records):
    cannot = {
        "in general": {"create", "search_drafts"},
        "public record": {
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "restricted record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "draft": {
            "read_draft",
            "draft_read_files",
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert denied(anonymous_visitor, records, cannot) == cannot


def test_logged_in_user_can(logged_in_user, records):
    can = {
        "in general": {"search_drafts"},
        "public record": {"read", "read_files"},
    }

    assert allowed(logged_in_user, records, can) == can


def test_logged_in_user_cannot(logged_in_user, records):
    cannot = {
        "in general": {"create"},
        "public record": {
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "restricted record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "draft": {
            "read_draft",
            "draft_read_files",
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert denied(logged_in_user, records, cannot) == cannot


def test_record_owner_can(record_owner, records):
    can = {
        "in general": {"search_drafts"},
        "public record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "restricted record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "draft": {
            "read_draft",
            "draft_read_files",
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert allowed(record_owner, records, can) == can


def test_record_owner_cannot(record_owner, records):
    cannot = {
        "in general": {"create"},
    }

    assert denied(record_owner, records, cannot) == cannot


def test_depositor_can(depositor, records):
    can = {
        "in general": {"create", "search_drafts"},
        "public record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "restricted record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "draft": {
            "read_draft",
            "draft_read_files",
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert allowed(depositor, records, can) == can


def test_depositor_cannot(depositor, records):
    cannot = {}

    assert denied(depositor, records, cannot) == cannot


def test_curator_can(curator, records):
    can = {
        "in general": {"search_drafts"},
        "public record": {"read", "read_files", "edit", "new_version"},
        "restricted record": {"edit", "new_version"},
        "draft": {
            "read_draft",
            "draft_read_files",
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert allowed(curator, records, can) == can


def test_curator_cannot(curator, records):
    cannot = {
        "in general": {"create"},
        "public record": {"delete", "delete_files", "lift_embargo"},
        "restricted record": {
            "read",
            "read_files",
            "delete",
            "delete_files",
            "lift_embargo",
        },
    }

    assert denied(curator, records, cannot) == cannot


def test_viewer_can(viewer, records):
    can = {
        "in general": {"create", "search_drafts"},
        "public record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "restricted record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "draft": {
            "read_draft",
            "draft_read_files",
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert allowed(viewer, records, can) == can


def test_viewer_cannot(viewer, records):
    cannot = {}

    assert denied(viewer, records, cannot) == cannot


def test_superuser_can(superuser, records):
    can = {
        "in general": {"create", "search_drafts"},
        "public record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "restricted record": {
            "read",
            "read_files",
            "edit",
            "new_version",
            "delete",
            "delete_files",
            "lift_embargo",
        },
        "draft": {
            "read_draft",
            "draft_read_files",
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert allowed(superuser, records, can) == can


def test_superuser_cannot(superuser, records):
    cannot = {
        "in general": {"update", "create_files", "update_files"},
    }

    assert denied(superuser, records, cannot) == cannot
