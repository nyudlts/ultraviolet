from flask import render_template_string

def test_small_file_download_visibility(create_app):
    app = create_app()
    app.config['SERVER_NAME'] = 'localhost'

    with app.app_context():

        file = {
            "size": 20 * 1024**3,
            "key": "example-file-key"
        }

        context = {
            "files": [file],
            "pid": "example-pid",
            "is_preview": True,
            "with_preview": True,
            "file_type": "jpg",
            "config": app.config,
            "record": {
                "links":{
                    "archive": "https://127.0.0.1:5000/api/records/6se1e-bgq09/files",
                        }
                },
        }

        wrapped_content = """
        {% from "invenio_app_rdm/records/macros/files.html" import file_list %}
        {{ file_list(files, pid, is_preview=true, record=record) }}
        """

        rendered = render_template_string(wrapped_content, **context)
        assert "Download" in rendered, f"Download button not found in rendered content: {rendered}"
        assert "wrap-long-link" in rendered, f"Download link not found in rendered content: {rendered}"
        assert "Download all" in rendered, f"Download all button not found in rendered content: {rendered}"

    
def test_large_filedownload_visibility(create_app):
    app = create_app()
    app.config['SERVER_NAME'] = 'localhost'

    with app.app_context():

        file = {
            "size": 60 * 1024**3,
            "key": "example-file-key"
        }
        context = {
            "files": [file],
            "pid": "example-pid",
            "is_preview": True,
            "with_preview": True,
            "file_type": "jpg",
            "config": app.config,
            "record": {
                "links":{
                    "archive": "https://127.0.0.1:5000/api/records/6se1e-bgq09/files",
                        }
                },
        }

        wrapped_content = """
        {% from "invenio_app_rdm/records/macros/files.html" import file_list %}
        {{ file_list(files, pid, is_preview=true, record=record) }}
        """

        rendered = render_template_string(wrapped_content, **context)
        assert "Download" not in rendered, f"Download button found in rendered content when it shouldn't be: {rendered}"
        assert not "wrap-long-link" in rendered, f"Download link found in rendered content: {rendered}"
        assert not "Download all" in rendered, f"Download all link found in rendered content: {rendered}"
