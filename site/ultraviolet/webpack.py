"""JS/CSS Webpack bundles for UltraViolet."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                # Add your webpack entrypoints
                "ultraviolet.deposit": "./js/ultraviolet/ultraviolet.deposit.js"
            },
        ),
    },
)
