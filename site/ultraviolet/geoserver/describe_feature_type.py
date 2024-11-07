import urllib

from flask import request, Response
from flask.views import MethodView

import requests


class DescribeFeatureType(MethodView):
    """GeoServer view."""

    def post(self):
        """Return JSON"""
        url = request.form.get('url', default=None)
        layers = request.form.get('layers', default=None)

        query_string = urllib.parse.urlencode({
            "outputFormat": "application/json",
            "request": "DescribeFeatureType",
            "service": "WFS",
            "typeName": layers,
            "version": "1.1.0",
        })

        response = requests.get("{0}?{1}".format(url, query_string))

        return Response(response.text, mimetype='application/json')
