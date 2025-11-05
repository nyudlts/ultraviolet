"""JS/CSS Webpack bundles for ultraviolet."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "mirador_js": "./js/ultraviolet/mirador.js",
                "mirador_css": "./css/ultraviolet/mirador.css"
            },
        ),
    },
)
