from invenio_access.permissions import system_identity


def test_public_map_view(app, service, minimal_record, client_with_login):
    data = minimal_record.copy()
    data["metadata"]["title"] = "Geospatial Data"
    data["custom_fields"] = {
        "geoserver:has_wms_layer": True,
        "geoserver:has_wfs_layer": True,
        "geoserver:layer_name": "sdr:nyu_2451_34156",
        "geoserver:bounds": "ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)"
    }

    draft = service.create(system_identity, data)
    record = service.publish(system_identity, draft.id)

    record_view = client_with_login.get("/records/" + record['id']).data
    html = record_view.decode("utf-8")

    assert "Geospatial Data" in html
    assert "data-wms-url=\"https://maps-public.geo.nyu.edu/geoserver/sdr/wms\"" in html
    assert "data-layer-name=\"sdr:nyu_2451_34156\"" in html
    assert "data-bounds=\"ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)\"" in html

def test_restricted_map_view(app, service, minimal_record, client_with_login):
    data = minimal_record.copy()
    data["access"]["files"] = "restricted"
    data["metadata"]["title"] = "Geospatial Data"
    data["custom_fields"] = {
        "geoserver:has_wms_layer": True,
        "geoserver:has_wfs_layer": True,
        "geoserver:layer_name": "sdr:nyu_2451_34156",
        "geoserver:bounds": "ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)"
    }

    draft = service.create(system_identity, data)
    record = service.publish(system_identity, draft.id)

    record_view = client_with_login.get("/records/" + record['id']).data
    html = record_view.decode("utf-8")

    assert "Geospatial Data" in html
    assert "data-wms-url=\"https://maps-restricted.geo.nyu.edu/geoserver/sdr/wms\"" in html
    assert "data-layer-name=\"sdr:nyu_2451_34156\"" in html
    assert "data-bounds=\"ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)\"" in html
