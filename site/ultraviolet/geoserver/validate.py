from __future__ import annotations

import json
import typing
import urllib

import requests
from flask import current_app
from marshmallow.exceptions import ValidationError
from marshmallow.validate import Validator

_T = typing.TypeVar("_T")


class ExperimentsValidator(Validator):
    default_message = "{type} layer {input} not found on {server}."

    def __init__(self, *, server: str | None = None, error: str | None = None):
        self.server = server
        self.error: str = error or self.default_message

    def _repr_args(self) -> str:
        return f"server={self.server!r}"

    def _format_error(self, service: str, value: _T) -> str:
        return self.error.format(service=service, input=value, server=self.server)

    def __call__(self, value: _T) -> _T:
        current_app.logger.debug(f"Validating {value}")

        raise ValidationError("Single string error message")
        # raise ValidationError(["Error messages one", "Error messages two"])
        # raise ValidationError({
        #     "one": "foo",
        #     "two": "bar",
        # })

        # raise ValidationError(
        #     "there was a problem",
        #     "custom_fields.experiments.layer"
        # )

        # raise ValidationError({
        #     "custom_fields.experiments.layer": "There was a problem with the layer name."
        # })

        # raise ValidationError(
        #     "blah blah blah",
        #     field_name="custom_fields.experiments.layer",
        # )

        # raise ValidationError({"custom_fields": {"experiments": {"layer": "layer error message"}}})
        # raise ValidationError({"experiments": {"layer": "layer error message"}})
        # raise ValidationError({"custom_fields.experiments.layer": "layer error message"})

        errors = []

        layer = value.get("layer", None)
        has_wms = value.get("has_wms", False)
        has_wfs = value.get("has_wfs", False)

        if has_wms:
            url = "{0}/wms".format(self.server)
            query_string = urllib.parse.urlencode({
                "service": "WMS",
                "version": "1.1.1",
                "request": "DescribeLayer",
                "layers": layer,
                "outputFormat": "application/json",
                "exceptions": "application/json",
            })

            full_url = "{0}?{1}".format(url, query_string)
            response = requests.get(full_url)
            data = json.loads(response.text)

            if data.get("exceptions") is not None:
                errors.append("Can't find WMS layer named {0}.".format(layer))

        if has_wfs:
            url = "{0}/wfs".format(self.server)
            query_string = urllib.parse.urlencode({
                "service": "WFS",
                "version": "2.0.0",
                "request": "DescribeFeatureType",
                "typename": layer,
                "outputFormat": "application/json",
                "exceptions": "application/json",
            })

            full_url = "{0}?{1}".format(url, query_string)
            response = requests.get(full_url)
            data = json.loads(response.text)

            if data.get("exceptions") is not None:
                errors.append("Can't find WFS layer named {0}.".format(layer))

        if len(errors) > 0:
            raise ValidationError(" ".join(errors))

        return value
