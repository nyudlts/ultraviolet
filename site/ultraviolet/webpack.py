"""JS/CSS Webpack bundles for ultraviolet."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={"web_archive_css": "./css/ultraviolet/web_archive.css"},
            dependencies={
                "replaywebpage": "^2.3.16",
            },
            copy=[
                {
                    "from": "../node_modules/replaywebpage",
                    "to": "../../static/js/replaywebpage",
                },
            ],
        ),
    },
)
