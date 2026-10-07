"""GLTF rendering."""

from flask import render_template
from invenio_previewer.proxies import current_previewer

previewable_extensions = ["gltf", "glb"]


def can_preview(file):
    """Check if file can be previewed."""
    return file.is_local() and (
        file.has_extensions(".gltf") or file.has_extensions(".glb")
    )


def preview(file):
    """Render Markdown."""
    return render_template(
        "ultraviolet/gltf.html",
        file=file,
        js_bundles=current_previewer.js_bundles + ["gltf_js.js"],
        css_bundles=current_previewer.css_bundles + ["gltf_css.css"],
    )
