# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for DOI email notification"""


from invenio_rdm_records.proxies import current_rdm_records_service
from ultraviolet.celery_tasks.tasks import poll_doi_until_registered
import ultraviolet.celery_tasks.tasks
import celery



def test_poll_doi_task(admin, caplog, minimal_record, client_with_login, services, app, db):
    """Test that publish a record with a DOI triggers the poll task and send notification."""

    service = current_rdm_records_service

    # Create + publish record with fake DOI
    data = minimal_record.copy()
    identity = admin.identity
    draft = service.create(identity, data)
    draft = service.pids.create(identity, draft.id, "doi")
    record = service.publish(id_=draft.id, identity=identity)

    assert "doi" in record._record.parent.pids
    print(caplog.messages)
    assert any(
        "Email dispatched to admin@inveniosoftware.org" in message
        for message in caplog.messages
    )

def test_poll_doi_task_status_reserved(monkeypatch, admin, caplog, minimal_record, client_with_login, services, app, db):
    """Test that publish a record with a DOI triggers the poll task but no email is sent if status is reserved."""

    # Monkeypatch the status check to always return "reserved"
    monkeypatch.setattr(
        "ultraviolet.celery_tasks.tasks.get_doi_status",
        lambda doi, test_mode=True: "reserved"
    )

    service = current_rdm_records_service

    # Create and publish record
    data = minimal_record.copy()
    identity = admin.identity
    draft = service.create(identity, data)
    draft = service.pids.create(identity, draft.id, "doi")
    record = service.publish(id_=draft.id, identity=identity)

    assert "doi" in record._record.parent.pids

    caplog.set_level("WARNING", logger="ultraviolet.celery_tasks.tasks")

    # Assert email is NOT sent due to "reserved" status
    assert all(
        "Email dispatched to admin@inveniosoftware.org" not in msg
        for msg in caplog.messages
    )

    assert any(
        "DOI status is 'reserved', not ready, retrying..." in msg
        for msg in caplog.messages
    )


def test_poll_doi_retries_then_succeeds(monkeypatch, app, db):
    """Test the task retries a few times when status is 'reserved' and eventually succeeds with 'registered'."""

    # 1: Enable eager mode and fake the worker context
    # monkeypatch.setattr(celery_app.conf, 'task_always_eager', True)
    monkeypatch.setattr(celery.app.task.Context, 'called_directly', False)

    # 2: Track number of times get_doi_status is called
    call_counter = {"count": 0}

    def fake_get_doi_status(doi, test_mode=True):
        call_counter["count"] += 1
        if call_counter["count"] < 4:
            return "reserved"
        return "registered"

    monkeypatch.setattr(
        "ultraviolet.celery_tasks.tasks.get_doi_status",
        fake_get_doi_status
    )

    # 3: Monkeypatch fetch_record_dict and extract_owner_email with minimal dummy data
    monkeypatch.setattr(
        "ultraviolet.celery_tasks.tasks.fetch_record_dict",
        lambda recid: {
            "pids": {"doi": {"identifier": "10.1234/fake.doi"}},
            "parent": {"access": {"owned_by": {"user": 1}}}
        }
    )

    monkeypatch.setattr(
        "ultraviolet.celery_tasks.tasks.extract_owner_email",
        lambda record_dict: "admin@inveniosoftware.org"
    )

    # 4: Patch send_email to record if it's sent
    sent_emails = []

    def fake_send_email(payload):
        sent_emails.append(payload)

    monkeypatch.setattr("ultraviolet.celery_tasks.tasks.send_email.delay", fake_send_email)

    # 5: Run the task via `.delay()` which now behaves like a real worker
    poll_doi_until_registered.delay("some-recid")

    # Step 6: Assertions
    assert call_counter["count"] == 4  # 3 retries, 1 success
    assert len(sent_emails) == 1
    assert "10." in sent_emails[0]["subject"]
    assert "registered" in sent_emails[0]["body"]

