import pytest
import responses
from marshmallow import ValidationError
from ultraviolet.geoserver.validate import BoundsValidator
from ultraviolet.geoserver.validate import LayerValidator


def test_layer_none():
    validator = LayerValidator(
        public_server="https://public.geoserver.org/geoserver/sdr",
        restricted_server="https://restricted.geoserver.org/geoserver/sdr",
    )
    assert validator(None) is None


def test_layer_empty():
    validator = LayerValidator(
        public_server="https://public.geoserver.org/geoserver/sdr",
        restricted_server="https://restricted.geoserver.org/geoserver/sdr",
    )
    assert validator("") is ""


@responses.activate
def test_only_public_layer_exists(
    valid_wms_response, valid_wfs_response, invalid_wms_response, invalid_wfs_response
):
    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wms",
        json=valid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wfs",
        json=valid_wfs_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wms",
        json=invalid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wfs",
        json=invalid_wfs_response,
        status=400,
    )

    validator = LayerValidator(
        public_server="https://public.geoserver.org/geoserver/sdr",
        restricted_server="https://restricted.geoserver.org/geoserver/sdr",
    )
    assert validator("sdr:nyu_2451_41645") == "sdr:nyu_2451_41645"


@responses.activate
def test_only_restricted_layer_exists(
    valid_wms_response, valid_wfs_response, invalid_wms_response, invalid_wfs_response
):
    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wms",
        json=invalid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wfs",
        json=invalid_wfs_response,
        status=400,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wms",
        json=valid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wfs",
        json=valid_wfs_response,
        status=200,
    )

    validator = LayerValidator(
        public_server="https://public.geoserver.org/geoserver/sdr",
        restricted_server="https://restricted.geoserver.org/geoserver/sdr",
    )
    assert validator("sdr:nyu_2451_41645") == "sdr:nyu_2451_41645"


@responses.activate
def test_layer_does_not_exist(invalid_wms_response, invalid_wfs_response):
    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wms",
        json=invalid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wfs",
        json=invalid_wfs_response,
        status=400,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wms",
        json=invalid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wfs",
        json=invalid_wfs_response,
        status=400,
    )

    validator = LayerValidator(
        public_server="https://public.geoserver.org/geoserver/sdr",
        restricted_server="https://restricted.geoserver.org/geoserver/sdr",
    )

    with pytest.raises(ValidationError):
        validator("sdr:foo_bar")


@responses.activate
def test_only_public_wfs_exists(
    invalid_wms_response, valid_wfs_response, invalid_wfs_response
):
    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wms",
        json=invalid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://public.geoserver.org/geoserver/sdr/wfs",
        json=valid_wfs_response,
        status=400,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wms",
        json=invalid_wms_response,
        status=200,
    )

    responses.add(
        method=responses.GET,
        url="https://restricted.geoserver.org/geoserver/sdr/wfs",
        json=invalid_wfs_response,
        status=400,
    )

    validator = LayerValidator(
        public_server="https://public.geoserver.org/geoserver/sdr",
        restricted_server="https://restricted.geoserver.org/geoserver/sdr",
    )

    with pytest.raises(ValidationError):
        validator("sdr:foo_bar")


def test_bounds_valid_decimals():
    validator = BoundsValidator()

    assert (
        validator(
            "ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)"
        )
        == "ENVELOPE(-74.2556640887564, -73.700009054899, 40.9157739339836, 40.4960925239255)"
    )


def test_bounds_valid_integers():
    validator = BoundsValidator()

    assert validator("ENVELOPE(-74, -73, 40, 40)") == "ENVELOPE(-74, -73, 40, 40)"


def test_bounds_invalid():
    validator = BoundsValidator()

    with pytest.raises(ValidationError):
        validator(
            "ENVELOPE(-74.2556640887564 -73.700009054899 40.9157739339836 40.4960925239255)"
        )
