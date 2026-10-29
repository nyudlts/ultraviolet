import pytest
from permission_checks import disagreements, fixture_for, people_in

TABLE = "role_permissions.csv"


@pytest.mark.parametrize("role", people_in(TABLE))
def test_policy_matches_the_table(role, records, request):
    identity = request.getfixturevalue(fixture_for(role))

    assert disagreements(TABLE, role, identity, records) == []
