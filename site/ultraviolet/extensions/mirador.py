"""Mirador rendering."""

from flask import render_template

from invenio_previewer.proxies import current_previewer

previewable_extensions = ["tiff", "jpg"]


def can_preview(file):
    """Check if file can be previewed."""
    return file.is_local() and file.has_extensions(".tiff", ".jpg")


def preview(file):
    """Render Markdown."""
    return render_template(
        "ultraviolet/mirador.html",
        file=file,
        js_bundles=current_previewer.js_bundles + ["mirador_js.js"],
        css_bundles=current_previewer.css_bundles + ["mirador_css.css"],
    )
