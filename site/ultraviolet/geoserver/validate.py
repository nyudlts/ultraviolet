from __future__ import annotations

import json
import re
import typing
import urllib

import requests
from marshmallow.exceptions import ValidationError
from marshmallow.validate import Validator

_T = typing.TypeVar("_T")


class BoundsValidator(Validator):
    def __call__(self, value: _T) -> _T:
        if re.match(
            r"ENVELOPE\((-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)\)",
            value,
        ):
            return value
        else:
            raise ValidationError("Invalid bounds value")


class LayerValidator(Validator):
    default_message = "{type} layer {input} not found on {public_server}."

    def __init__(
        self,
        *,
        public_server: str | None = None,
        restricted_server: str | None = None,
        error: str | None = None,
    ):
        self.public_server = public_server
        self.restricted_server = restricted_server
        self.error: str = error or self.default_message

    def _repr_args(self) -> str:
        return f"public_server={self.public_server!r} restricted_server={self.restricted_server!r}"

    def _format_error(self, service: str, value: _T) -> str:
        return self.error.format(
            service=service,
            input=value,
            public_server=self.public_server,
            restricted_server=self.restricted_server,
        )

    def __call__(self, value: _T) -> _T:
        if value is None:
            return None

        if value is "":
            return ""

        public_errors = []
        restricted_errors = []

        # Public Servers
        url = "{0}/wms".format(self.public_server)
        query_string = urllib.parse.urlencode(
            {
                "service": "WMS",
                "version": "1.1.1",
                "request": "DescribeLayer",
                "layers": value,
                "outputFormat": "application/json",
                "exceptions": "application/json",
            }
        )

        full_url = "{0}?{1}".format(url, query_string)
        response = requests.get(full_url)
        data = json.loads(response.text)

        if data.get("exceptions") is not None:
            public_errors.append("Can't find WMS layer named {0}.".format(value))

        url = "{0}/wfs".format(self.public_server)
        query_string = urllib.parse.urlencode(
            {
                "service": "WFS",
                "version": "2.0.0",
                "request": "DescribeFeatureType",
                "typename": value,
                "outputFormat": "application/json",
                "exceptions": "application/json",
            }
        )

        full_url = "{0}?{1}".format(url, query_string)
        response = requests.get(full_url)
        data = json.loads(response.text)

        if data.get("exceptions") is not None:
            public_errors.append("Can't find WFS layer named {0}.".format(value))

        # Restricted Servers
        url = "{0}/wms".format(self.restricted_server)
        query_string = urllib.parse.urlencode(
            {
                "service": "WMS",
                "version": "1.1.1",
                "request": "DescribeLayer",
                "layers": value,
                "outputFormat": "application/json",
                "exceptions": "application/json",
            }
        )

        full_url = "{0}?{1}".format(url, query_string)
        response = requests.get(full_url)
        data = json.loads(response.text)

        if data.get("exceptions") is not None:
            restricted_errors.append("Can't find WMS layer named {0}.".format(value))

        url = "{0}/wfs".format(self.restricted_server)
        query_string = urllib.parse.urlencode(
            {
                "service": "WFS",
                "version": "2.0.0",
                "request": "DescribeFeatureType",
                "typename": value,
                "outputFormat": "application/json",
                "exceptions": "application/json",
            }
        )

        full_url = "{0}?{1}".format(url, query_string)
        response = requests.get(full_url)
        data = json.loads(response.text)

        if data.get("exceptions") is not None:
            restricted_errors.append("Can't find WFS layer named {0}.".format(value))

        if len(public_errors) > 0 and len(restricted_errors) > 0:
            raise ValidationError(
                "Neither a WMS or WFS layer named {0} exists on {1} ".format(
                    value, self.public_server
                )
            )

        return value
