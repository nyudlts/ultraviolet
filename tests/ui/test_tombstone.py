from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_access.permissions import system_identity
import time

def test_tombstone_page(full_record, client_with_login, services, app, db):
    """
    Test for display metadata of a delete record on its tombstone page.
    DOI is skipped. 
    """

    service = current_rdm_records_service

    data = full_record.copy()

    # Skip checks for DOI
    if "doi" in data["pids"]:
        del data["pids"]["doi"]
    draft = service.create(system_identity, data)
    record = service.publish(system_identity, draft.id)

    tombstone_info = {
        "note": "A given note by staff",
        "removal_reason": {"id": "copyright"}
    }

    time.sleep(5)

    service.delete_record(system_identity, record.id, data=tombstone_info)

    response = client_with_login.get("/records/" + record['id'])
    html = response.data.decode("utf-8")

    assert "The record you are trying to access was removed" in html

    # Check for removal note and reason
    assert "A given note by staff" in html
    assert "Reason for removal" in html

    # Check if all metadata fields are displayed
    # **Title**
    assert full_record['metadata']['title'] in html

    # **Additional Titles**
    for title in full_record['metadata']['additional_titles']:
        assert title["title"] in html

    # **Description**
    assert full_record['metadata']['description'] in html

    # **Additional Descriptions**
    for desc in full_record['metadata']['additional_descriptions']:
        assert desc["description"] in html

    # **Publication Date**
    assert full_record['metadata']['publication_date'] in html

    # **Publisher**
    assert full_record['metadata']['publisher'] in html

    # **Version**
    assert full_record['metadata']['version'] in html

    # **Resource Type**
    assert 'Photo' in html

    # **Creators**
    for creator in full_record['metadata']['creators']:
        assert creator["person_or_org"]["name"] in html

    # **Contributors**
    for contributor in full_record['metadata']['contributors']:
        assert contributor["person_or_org"]["name"] in html

    # **Identifiers**
    for identifier in full_record['metadata']['identifiers']:
        assert identifier["identifier"] in html

    # **Related Identifiers**
    for related in full_record['metadata']['related_identifiers']:
        assert related["identifier"] in html
        assert 'Is cited by' in html

    # **Dates**
    for date in full_record['metadata']['dates']:
        assert date["date"] in html
        assert 'Other' in html

    # **Languages**
    assert 'Danish' in html
    assert 'English' in html

    # **Subjects**
    for subject in full_record['metadata']['subjects']:
        if "id" in subject:
            assert 'Abdominal Injuries (MeSH)' in html
        if "subject" in subject:
            assert subject["subject"] in html

    # **Rights**
    for right in full_record['metadata']['rights']:
        if "title" in right and "en" in right["title"]:
            assert right["title"]["en"] in html
        if "description" in right and "en" in right["description"]:
            assert right["description"]["en"] in html

    # **References**
    for reference in full_record['metadata']['references']:
        assert reference["reference"] in html

    # **Funding**
    for funding in full_record['metadata']['funding']:
        assert funding["funder"]["id"] in html
        assert funding["award"]["id"] in html

    # **Locations**
    for location in full_record['metadata']['locations']['features']:
        assert location["place"] in html
        assert location["description"] in html
        for identifier in location["identifiers"]:
            assert identifier["identifier"] in html

    # **Sizes**
    for size in full_record['metadata']['sizes']:
        assert size in html

    # **Formats**
    for file_format in full_record['metadata']['formats']:
        assert file_format in html

    # Skip checks for DOI
    # assert full_record['pids']['doi']['identifier'] in html
