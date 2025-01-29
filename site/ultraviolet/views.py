"""Additional views."""

from flask import Blueprint

from .geoserver.describe_feature_type import DescribeFeatureType
from .geoserver.describe_layer import DescribeLayer
from .geoserver.get_feature_info import GetFeatureInfo


#
# Registration
#
def create_blueprint(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "ultraviolet",
        __name__,
        template_folder="./templates",
    )

    blueprint.add_url_rule(
        "/geoserver/describe_feature_type",
        view_func=DescribeFeatureType.as_view("describe_feature_type"),
    )

    blueprint.add_url_rule(
        "/geoserver/get_feature_info",
        view_func=GetFeatureInfo.as_view("get_feature_info"),
    )

    blueprint.add_url_rule(
        "/geoserver/describe_layer",
        view_func=DescribeLayer.as_view("describe_layer"),
    )

    return blueprint
