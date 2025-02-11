from __future__ import annotations

import json
import typing
import urllib

import requests
from marshmallow.exceptions import ValidationError
from marshmallow.validate import Validator

_T = typing.TypeVar("_T")


class BoundsValidator(Validator):
    def __call__(self, value: _T) -> _T:
        return value


class LayerValidator(Validator):
    default_message = "{type} layer {input} not found on {server}."

    def __init__(self, *, server: str | None = None, error: str | None = None):
        self.server = server
        self.error: str = error or self.default_message

    def _repr_args(self) -> str:
        return f"server={self.server!r}"

    def _format_error(self, service: str, value: _T) -> str:
        return self.error.format(service=service, input=value, server=self.server)

    def __call__(self, value: _T) -> _T:
        if value is None:
            return None

        if value is "":
            return ""

        errors = []

        url = "{0}/wms".format(self.server)
        query_string = urllib.parse.urlencode({
            "service": "WMS",
            "version": "1.1.1",
            "request": "DescribeLayer",
            "layers": value,
            "outputFormat": "application/json",
            "exceptions": "application/json",
        })

        full_url = "{0}?{1}".format(url, query_string)
        response = requests.get(full_url)
        data = json.loads(response.text)

        if data.get("exceptions") is not None:
            errors.append("Can't find WMS layer named {0}.".format(value))

        url = "{0}/wfs".format(self.server)
        query_string = urllib.parse.urlencode({
            "service": "WFS",
            "version": "2.0.0",
            "request": "DescribeFeatureType",
            "typename": value,
            "outputFormat": "application/json",
            "exceptions": "application/json",
        })

        full_url = "{0}?{1}".format(url, query_string)
        response = requests.get(full_url)
        data = json.loads(response.text)

        if data.get("exceptions") is not None:
            errors.append("Can't find WFS layer named {0}.".format(value))

        if len(errors) > 0:
            raise ValidationError("Neither a WMS or WFS layer named {0} exists on {1} ".format(value, self.server))

        return value
