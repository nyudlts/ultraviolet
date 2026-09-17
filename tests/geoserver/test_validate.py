import pytest
import responses
from marshmallow import ValidationError

from ultraviolet.geoserver.validate import BoundsValidator
from ultraviolet.geoserver.validate import WmsLayerValidator
from ultraviolet.geoserver.validate import WfsLayerValidator


def test_wms_layer_none():
    validator = WmsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator(None) is None


def test_wms_layer_empty():
    validator = WmsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator("") is ""


@responses.activate
def test_only_public_wms_layer_exists(valid_public_wms, invalid_restricted_wms):
    validator = WmsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator("sdr:nyu_2451_41645") == "sdr:nyu_2451_41645"


@responses.activate
def test_only_restricted_wms_layer_exists(invalid_public_wms, valid_restricted_wms):
    validator = WmsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator("sdr:nyu_2451_41645") == "sdr:nyu_2451_41645"


@responses.activate
def test_wms_layer_does_not_exist(
    invalid_public_wms,
    invalid_restricted_wms,
):
    validator = WmsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )

    with pytest.raises(ValidationError):
        validator("sdr:foo_bar")


@responses.activate
def test_wms_layer_connection_error_raises_validation_error():
    responses.get(
        url="https://maps-public.geo.nyu.edu/geoserver/sdr/wms",
        body=responses.ConnectionError("public server unreachable"),
    )
    responses.get(
        url="https://maps-restricted.geo.nyu.edu/geoserver/sdr/wms",
        body=responses.ConnectionError("restricted server unreachable"),
    )

    validator = WmsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )

    with pytest.raises(
        ValidationError,
        match="Public server not reachable for validation: https://maps-public.geo.nyu.edu/geoserver/sdr",
    ):
        validator("sdr:foo_bar")


def test_wfs_layer_none():
    validator = WfsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator(None) is None


def test_wfs_layer_empty():
    validator = WfsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator("") is ""


@responses.activate
def test_only_public_wfs_layer_exists(valid_public_wfs, invalid_restricted_wfs):
    validator = WfsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator("sdr:nyu_2451_41645") == "sdr:nyu_2451_41645"


@responses.activate
def test_only_restricted_wfs_layer_exists(invalid_public_wfs, valid_restricted_wfs):
    validator = WfsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )
    assert validator("sdr:nyu_2451_41645") == "sdr:nyu_2451_41645"


@responses.activate
def test_layer_does_not_exist(
    invalid_public_wfs,
    invalid_restricted_wfs,
):
    validator = WfsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )

    with pytest.raises(ValidationError):
        validator("sdr:foo_bar")


@responses.activate
def test_wfs_layer_connection_error_raises_validation_error():
    responses.get(
        url="https://maps-public.geo.nyu.edu/geoserver/sdr/wfs",
        body=responses.ConnectionError("public server unreachable"),
    )
    responses.get(
        url="https://maps-restricted.geo.nyu.edu/geoserver/sdr/wfs",
        body=responses.ConnectionError("restricted server unreachable"),
    )

    validator = WfsLayerValidator(
        public_server="https://maps-public.geo.nyu.edu/geoserver/sdr",
        restricted_server="https://maps-restricted.geo.nyu.edu/geoserver/sdr",
    )

    with pytest.raises(
        ValidationError,
        match="Public server not reachable for validation: https://maps-public.geo.nyu.edu/geoserver/sdr",
    ):
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
