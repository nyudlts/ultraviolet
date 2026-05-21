"""Mirador rendering."""

from flask import current_app, render_template


def can_preview(file):
    """Check if file can be previewed."""
    extensions = map(
        lambda extension: ".{0}".format(extension),
        current_app.config.get(
            "RDM_IIIF_MANIFEST_FORMATS",
            [
                "jpg",
                "jpeg",
                "jp2",
                "png",
                "tif",
                "tiff",
            ],
        ),
    )

    return file.is_local() and file.has_extensions(*extensions)


def preview(file):
    """Render Markdown."""
    return render_template(
        "ultraviolet/mirador.html",
        file=file,
    )
