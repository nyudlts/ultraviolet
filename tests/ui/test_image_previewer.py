# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""View tests of the front page."""

from io import BytesIO

from PIL import Image
from invenio_access.permissions import system_identity
from invenio_rdm_records.proxies import current_rdm_records_service


def test_image_previewer(
    minimal_record, client_with_login, services, app, db, register_file_service
):
    """
    Ensure the image previewer is configured correctly.
    """

    service = current_rdm_records_service

    data = minimal_record.copy()
    data["files"]["enabled"] = True

    draft = service.create(system_identity, data)

    # Add a file
    image = Image.new("RGB", (1, 1), color=(0, 0, 0))
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG", quality=1, optimize=True)

    service.draft_files.init_files(
        system_identity, draft.id, data=[{"key": "test.jpg"}]
    )
    service.draft_files.set_file_content(
        system_identity, draft.id, "test.jpg", image_bytes
    )
    service.draft_files.commit_file(system_identity, draft.id, "test.jpg")

    # Publish
    record = service.publish(system_identity, draft.id)

    preview = client_with_login.get(
        "/records/" + record["id"] + "/preview/test.jpg?include_deleted=0"
    ).data
    html = preview.decode("utf-8")

    assert "iiif-simple-preview" in html
