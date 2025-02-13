import pytest
import responses
from marshmallow import ValidationError
from ultraviolet.geoserver.validate import BoundsValidator
from ultraviolet.geoserver.validate import LayerValidator


@pytest.fixture
def valid_wms_response():
    return {
        "version": "1.1.1",
        "layerDescriptions": [
            {
                "layerName": "nyu_2451_41645",
                "owsURL": "https://fake-geoserver.org/geoserver/sdr/wfs?",
                "owsType": "WFS",
                "typeName": "nyu_2451_41645"
            }
        ]
    }


@pytest.fixture
def valid_wfs_response():
    return {
        "elementFormDefault": "qualified",
        "targetNamespace": "geo.nyu.edu",
        "targetPrefix": "sdr",
        "featureTypes": [
            {
                "typeName": "nyu_2451_41645",
                "properties": [
                    {
                        "name": "fieldname",
                        "maxOccurs": 1,
                        "minOccurs": 0,
                        "nillable": True,
                        "type": "xsd:int",
                        "localType": "int"
                    }
                ]
            }
        ]
    }


@pytest.fixture
def invalid_wms_response():
    return {
        "version": "1.1.1",
        "exceptions": [
            {
                "code": "LayerNotDefined",
                "locator": "MapLayerInfoKvpParser",
                "text": "sdr:foo_bar: no such layer on this server"
            }
        ]
    }


@pytest.fixture
def invalid_wfs_response():
    return {
        "version": "2.0.0",
        "exceptions": [
            {
                "code": "InvalidParameterValue",
                "locator": "DescribeFeatureType",
                "text": "Could not find type: sdr:foo_bar"
            }
        ]
    }


def test_layer_none():
    validator = LayerValidator(server="https://fake-geoserver.org/geoserver/sdr")
    assert validator(None) is None


def test_layer_empty():
    validator = LayerValidator(server="https://fake-geoserver.org/geoserver/sdr")
    assert validator("") is ""


@responses.activate
def test_layer_valid(valid_wms_response, valid_wfs_response):
    responses.add(
        method=responses.GET,
        url='https://fake-geoserver.org/geoserver/sdr/wms',
        json=valid_wms_response,
        status=200
    )

    responses.add(
        method=responses.GET,
        url='https://fake-geoserver.org/geoserver/sdr/wfs',
        json=valid_wfs_response,
        status=200
    )

    validator = LayerValidator(server="https://fake-geoserver.org/geoserver/sdr")
    assert validator("sdr:nyu_2451_41645") == "sdr:nyu_2451_41645"


@responses.activate
def test_layer_invalid(invalid_wms_response, invalid_wfs_response):
    responses.add(
        method=responses.GET,
        url='https://fake-geoserver.org/geoserver/sdr/wms',
        json=invalid_wms_response,
        status=200
    )

    responses.add(
        method=responses.GET,
        url='https://fake-geoserver.org/geoserver/sdr/wfs',
        json=invalid_wfs_response,
        status=400
    )

    validator = LayerValidator(server="https://fake-geoserver.org/geoserver/sdr")

    with pytest.raises(ValidationError):
        validator("sdr:foo_bar")


@responses.activate
def test_layer_half_valid(invalid_wms_response, valid_wfs_response):
    responses.add(
        method=responses.GET,
        url='https://fake-geoserver.org/geoserver/sdr/wms',
        json=invalid_wms_response,
        status=200
    )

    responses.add(
        method=responses.GET,
        url='https://fake-geoserver.org/geoserver/sdr/wfs',
        json=valid_wfs_response,
        status=400
    )

    validator = LayerValidator(server="https://fake-geoserver.org/geoserver/sdr")

    with pytest.raises(ValidationError):
        validator("sdr:foo_bar")


def test_bounds_valid_decimals():
    validator = BoundsValidator()

    assert validator(
        "ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)") == "ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)"


def test_bounds_valid_integers():
    validator = BoundsValidator()

    assert validator(
        "ENVELOPE(-74, -73, 40, 40)") == "ENVELOPE(-74, -73, 40, 40)"


def test_bounds_invalid():
    validator = BoundsValidator()

    with pytest.raises(ValidationError):
        validator("ENVELOPE(-74.2556640887564 -73.700009054899 40.9157739339836 40.4960925239255)")
