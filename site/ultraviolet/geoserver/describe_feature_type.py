import urllib

import requests
from flask import request, Response
from flask.views import MethodView


class DescribeFeatureType(MethodView):
    """Proxy for GeoServer DescribeFeatureType requests."""

    def post(self):
        """Pass DescribeFeatureType requests to GeoServer and hand back results."""
        url = request.form.get("url", default=None)
        layers = request.form.get("layers", default=None)

        query_string = urllib.parse.urlencode(
            {
                "service": "WFS",
                "version": "1.1.0",
                "request": "DescribeFeatureType",
                "typeName": layers,
                "outputFormat": "application/json",
            }
        )

        response = requests.get("{0}?{1}".format(url, query_string))

        return Response(response.text, mimetype="application/json")
