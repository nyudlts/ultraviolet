import urllib

from flask import request, Response
from flask.views import MethodView

import requests


class GetFeatureInfo(MethodView):
    """GeoServer view."""

    def post(self):
        """Return JSON"""
        data = request.get_json()

        url = data.get('url', None)
        query_string = urllib.parse.urlencode({
            "service": "WMS",
            "version": "1.1.1",
            "request": "GetFeatureInfo",
            "layers": data.get('layers', None),
            "query_layers": data.get('layers', None),
            "bbox": data.get('bbox', None),
            "width": data.get('width', None),
            "height": data.get('height', None),
            "x": data.get('x', None),
            "y": data.get('y', None),
            "srs": "EPSG:4326",
            "info_format": "application/json",
            "styles": ""
        })

        response = requests.get("{0}?{1}".format(url, query_string))

        return Response(response.text, mimetype='application/json')
