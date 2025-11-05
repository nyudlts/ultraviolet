import json
from io import BytesIO

from PIL import Image
from invenio_access.permissions import system_identity
from invenio_rdm_records.proxies import current_rdm_records_service


def test_mirador_previewer(services, minimal_record, client_with_login):
    service = current_rdm_records_service

    data = minimal_record.copy()
    data["metadata"]["title"] = "IIIF Test Record"
    data["files"]["enabled"] = True

    draft = service.create(system_identity, data)

    for image_format in ["bmp", "gif", "jpeg", "png", "tiff"]:
        attach_image_file(draft, image_format, service)

    record = service.publish(system_identity, draft.id)

    # Previewer
    previewer = client_with_login.get(
        "/records/" + record['id'] + "/preview/test.bmp?include_deleted=0"
    ).data.decode("utf-8")

    assert "data-mirador-url=" in previewer
    assert "data-canvas-url=" in previewer

    # IIIF Manifest
    manifest_json = json.loads(client_with_login.get(
        "/api/iiif/record:" + record['id'] + "/manifest"
    ).data.decode("utf-8"))

    assert manifest_json["label"] == "IIIF Test Record"

    # Ensure file types show up in Manifest
    assert len(manifest_json["sequences"][0]["canvases"]) == 5
    assert manifest_json["sequences"][0]["canvases"][0]["label"] == "test.bmp"
    assert manifest_json["sequences"][0]["canvases"][1]["label"] == "test.gif"
    assert manifest_json["sequences"][0]["canvases"][2]["label"] == "test.jpeg"
    assert manifest_json["sequences"][0]["canvases"][3]["label"] == "test.png"
    assert manifest_json["sequences"][0]["canvases"][4]["label"] == "test.tiff"

    # TODO: Frame filename updates when image is changed
    # TODO: All image extensions show up in mirador previewer: X of Y


def attach_image_file(draft, image_format, service):
    image_file_name = "test.{0}".format(image_format)
    image_file = BytesIO()
    image = Image.new("RGB", (1280, 1024), (255, 0, 0, 0))
    image.save(image_file, image_format)
    image_file.seek(0)
    service.draft_files.init_files(system_identity, draft.id, data=[{"key": image_file_name}])
    service.draft_files.set_file_content(system_identity, draft.id, image_file_name, image_file)
    service.draft_files.commit_file(system_identity, draft.id, image_file_name)
