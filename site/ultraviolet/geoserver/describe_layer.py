import urllib

import requests
from flask import request, Response
from flask.views import MethodView


class DescribeLayer(MethodView):
    """Proxy for GeoServer DescribeLayer requests."""

    def post(self):
        """Pass DescribeLayer requests to GeoServer and hand back results."""
        url = request.form.get("url", default=None)
        layers = request.form.get("layers", default=None)

        query_string = urllib.parse.urlencode(
            {
                "service": "WMS",
                "version": "1.1.1",
                "request": "DescribeLayer",
                "layers": layers,
                "outputFormat": "application/json",
                "exceptions": "application/json",
            }
        )

        response = requests.get("{0}?{1}".format(url, query_string))

        return Response(response.text, mimetype="application/json")
