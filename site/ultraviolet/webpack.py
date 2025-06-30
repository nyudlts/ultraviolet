"""JS/CSS Webpack bundles for ultraviolet."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "geoserver_js": "./js/ultraviolet/geoserver.js",
                "geoserver_css": "./css/ultraviolet/geoserver.css",
                "web_archive_css": "./css/ultraviolet/web_archive.css"
            },
            dependencies={
                "leaflet": "^1.9.4",
                "ol": "^10.2.1"
            }
        ),
    },
)
