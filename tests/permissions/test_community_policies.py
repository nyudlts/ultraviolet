from permission_checks import allowed, denied


def test_community_reader_can(community_reader, community_records):
    can = {
        "in general": {"search_drafts"},
        "public record": {"read", "read_files"},
        "restricted record": {"read", "read_files"},
    }

    assert allowed(community_reader, community_records, can) == can


def test_community_reader_cannot(community_reader, community_records):
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

    assert denied(community_reader, community_records, cannot) == cannot


def test_community_curator_can(community_curator, community_records):
    can = {
        "in general": {"search_drafts"},
        "public record": {"read", "read_files", "edit", "new_version"},
        "restricted record": {"read", "read_files", "edit", "new_version"},
        "draft": {
            "update_draft",
            "draft_create_files",
            "pid_reserve",
            "publish",
            "delete_draft",
        },
    }

    assert allowed(community_curator, community_records, can) == can


def test_community_curator_cannot(community_curator, community_records):
    cannot = {
        "in general": {"create"},
        "public record": {"delete", "delete_files", "lift_embargo"},
        "restricted record": {"delete", "delete_files", "lift_embargo"},
        "draft": {"read_draft", "draft_read_files"},
    }

    assert denied(community_curator, community_records, cannot) == cannot


def test_community_manager_can(community_manager, community_records):
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

    assert allowed(community_manager, community_records, can) == can


def test_community_manager_cannot(community_manager, community_records):
    cannot = {
        "in general": {"create"},
    }

    assert denied(community_manager, community_records, cannot) == cannot


def test_community_owner_can(community_owner, community_records):
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

    assert allowed(community_owner, community_records, can) == can


def test_community_owner_cannot(community_owner, community_records):
    cannot = {
        "in general": {"create"},
    }

    assert denied(community_owner, community_records, cannot) == cannot


def test_member_of_another_community_can(
    member_of_another_community, community_records
):
    can = {
        "in general": {"search_drafts"},
        "public record": {"read", "read_files"},
    }

    assert allowed(member_of_another_community, community_records, can) == can


def test_member_of_another_community_cannot(
    member_of_another_community, community_records
):
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

    assert denied(member_of_another_community, community_records, cannot) == cannot
