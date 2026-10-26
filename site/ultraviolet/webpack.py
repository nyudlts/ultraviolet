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
                "gltf_js": "./js/ultraviolet/gltf.js",
                "gltf_css": "./css/ultraviolet/gltf.css",
            },
            dependencies={
                "leaflet": "^1.9.4",
                "ol": "^10.2.1",
                "@google/model-viewer": "^4.0.0",
            },
        ),
    },
)
