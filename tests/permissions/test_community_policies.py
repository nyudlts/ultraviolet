import pytest
from permission_checks import disagreements, fixture_for, people_in

TABLE = "community_permissions.csv"


@pytest.mark.parametrize("member", people_in(TABLE))
def test_policy_matches_the_table(member, community_records, request):
    identity = request.getfixturevalue(fixture_for(member))

    assert disagreements(TABLE, member, identity, community_records) == []
