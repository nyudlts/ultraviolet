import csv
import re
from pathlib import Path

from ultraviolet.policies import UltraVioletPermissionPolicy

ACTIONS = {
    "Start a new record": "create",
    "Search drafts": "search_drafts",
    "View the record": "read",
    "View and download its files": "read_files",
    "Edit the record": "edit",
    "Publish a new version": "new_version",
    "Delete the record": "delete",
    "Delete its files": "delete_files",
    "Lift its embargo": "lift_embargo",
    "View the draft": "read_draft",
    "View the draft's files": "draft_read_files",
    "Edit the draft": "update_draft",
    "Add files to the draft": "draft_create_files",
    "Reserve a DOI": "pid_reserve",
    "Publish the draft": "publish",
    "Discard the draft": "delete_draft",
    "Change a published record directly": "update",
    "Upload files outside a draft": "create_files",
    "Replace files outside a draft": "update_files",
}

RECORDS = {
    "In general": "in general",
    "A public record": "public record",
    "A restricted record": "restricted record",
    "A draft": "draft",
}


def read_table(filename):
    with open(Path(__file__).parent / filename, newline="") as table:
        return list(csv.DictReader(table))


def people_in(filename):
    return list(read_table(filename)[0])[2:]


def fixture_for(person):
    return re.sub(r"\W+", "_", person.lower())


def disagreements(filename, person, identity, records):
    found = []
    for row in read_table(filename):
        what = row["What they do"]
        on = row["On"]
        record = records[RECORDS[on]]
        policy = UltraVioletPermissionPolicy(ACTIONS[what], record=record)
        policy_says = "Yes" if policy.allows(identity) else "No"
        if policy_says != row[person]:
            found.append(
                f"{what} ({on}): the table says {row[person]} "
                f"for {person} but the policy says {policy_says}"
            )
    return found
