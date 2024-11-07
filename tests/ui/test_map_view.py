from invenio_access.permissions import system_identity


def test_map_view(app, service, minimal_record, client_with_login):
    data = minimal_record.copy()
    data["metadata"]["title"] = "Map View"

    draft = service.create(system_identity, data)
    record = service.publish(system_identity, draft.id)

    record_view = client_with_login.get("/records/" + record['id']).data
    html = record_view.decode("utf-8")

    assert "Map View" in html
