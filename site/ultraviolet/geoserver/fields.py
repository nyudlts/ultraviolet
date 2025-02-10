from invenio_records_resources.services.custom_fields import BaseListCF
from marshmallow import fields
from marshmallow_utils.fields import SanitizedUnicode

from ultraviolet.geoserver.validate import LayerValidator, BoundsValidator

from ultraviolet.geoserver.constants import PUBLIC_URL


class GeoServerCF(BaseListCF):
    """GeoServer with layer and bounds."""

    def __init__(self, name, **kwargs):
        """Constructor."""
        field_args = dict(
            dict(
                nested=dict(
                    layer=SanitizedUnicode(
                        validate=LayerValidator(server=PUBLIC_URL)
                    ),
                    bounds=SanitizedUnicode(
                        validate=BoundsValidator()
                    ),
                    has_wms=fields.Boolean(),
                    has_wfs=fields.Boolean(),
                )
            ),
            **(kwargs.get("field_args", {}))
        )

        kwargs.pop('field_args')

        super().__init__(
            name,
            field_cls=fields.Nested,
            field_args=field_args,
            multiple=False,
            **kwargs
        )

    @property
    def mapping(self):
        """Return the mapping."""
        return {
            "properties": {
                "layer": {
                    "type": "text"
                },
                "has_wms": {
                    "type": "boolean"
                },
                "has_wfs": {
                    "type": "boolean"
                },
                "bounds": {
                    "type": "text"
                },
            }
        }
