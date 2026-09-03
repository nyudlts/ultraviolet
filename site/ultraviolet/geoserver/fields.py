from invenio_records_resources.services.custom_fields import BaseListCF
from marshmallow import fields
from marshmallow_utils.fields import SanitizedUnicode

from ultraviolet.geoserver.validate import (
    WmsLayerValidator,
    BoundsValidator,
    WfsLayerValidator,
)


class GeoServerCF(BaseListCF):
    """GeoServer with layer and bounds."""

    def __init__(self, name, public_server, restricted_server, **kwargs):
        """Constructor."""
        field_args = dict(
            dict(
                nested=dict(
                    layer=SanitizedUnicode(
                        validate=(
                            WmsLayerValidator(
                                public_server=public_server,
                                restricted_server=restricted_server,
                            )
                        )
                    ),
                    wfs_layer=SanitizedUnicode(
                        validate=(
                            WfsLayerValidator(
                                public_server=public_server,
                                restricted_server=restricted_server,
                            )
                        )
                    ),
                    bounds=SanitizedUnicode(validate=BoundsValidator()),
                )
            ),
        )

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
                "layer": {"type": "text"},
                "wms_layer": {"type": "text"},
                "bounds": {"type": "text"},
            }
        }
