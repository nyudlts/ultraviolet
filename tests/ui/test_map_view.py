from invenio_access.permissions import system_identity


def test_public_map_view_when_anonymous(services, geospatial_record, client):
    published_record = publish_draft(geospatial_record, services)

    html = client.get("/records/" + published_record['id']).data.decode("utf-8")

    assert "Geospatial Data" in html
    assert "Web Services" in html

    assert "data-preview=\"True\"" in html
    assert "data-wms-url=\"https://maps-public.geo.nyu.edu/geoserver/sdr/wms\"" in html
    assert "data-layer-name=\"sdr:nyu_2451_34156\"" in html
    assert "data-bounds=\"ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)\"" in html


def test_restricted_map_view_when_logged_in(services, restricted_geospatial_record, client_with_login):
    published_record = publish_draft(restricted_geospatial_record, services)

    html = client_with_login.get("/records/" + published_record['id']).data.decode("utf-8")

    assert "Geospatial Data" in html
    assert "Web Services" in html

    assert "data-preview=\"True\"" in html
    assert "data-wms-url=\"https://maps-restricted.geo.nyu.edu/geoserver/sdr/wms\"" in html
    assert "data-layer-name=\"sdr:nyu_2451_34156\"" in html
    assert "data-bounds=\"ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)\"" in html


def test_restricted_map_view_when_anonymous(services, restricted_geospatial_record, client):
    published_record = publish_draft(restricted_geospatial_record, services)

    html = client.get("/records/" + published_record['id']).data.decode("utf-8")

    assert "Geospatial Data" in html
    assert "data-preview=\"False\"" in html
    assert "data-bounds=\"ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)\"" in html

    assert "Web Services" not in html
    assert "data-wms-url=\"https://maps-restricted.geo.nyu.edu/geoserver/sdr/wms\"" not in html
    assert "data-layer-name=\"sdr:nyu_2451_34156\"" not in html


def publish_draft(data, services):
    draft = services.create(system_identity, data)
    record = services.publish(system_identity, draft.id)

    return record
