
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 NYU.
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


import logging
import requests
from flask import current_app
from celery import signals

from invenio_access.permissions import system_identity
from invenio_rdm_records.proxies import current_rdm_records
from invenio_pidstore.errors import PersistentIdentifierError
from invenio_mail.tasks import send_email
from invenio_accounts.proxies import current_datastore


logger = logging.getLogger(__name__)

# === Helper Functions ===

def fetch_record_dict(recid):
    return current_rdm_records.records_service.read(identity=system_identity, id_=recid).to_dict()

def extract_owner_email(record_dict):
    try:
        owner_id = record_dict.get("parent", {}).get("access", {}).get("owned_by", {}).get("user")
    except Exception as e:
        logger.warning(f"[DOI Polling Task] Error extracting owner ID: {e}")
        return None
    
    if not owner_id:
        return None
    user = current_datastore.get_user(owner_id)
    return user.email if user else None

def get_doi_status(doi, test_mode=True):
    base = "https://api.test.datacite.org" if test_mode else "https://api.datacite.org"
    url = f"{base}/dois/{doi}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["data"]["attributes"]["state"]

def get_random_test_doi():
    url = "https://api.test.datacite.org/dois?random=true&page[size]=1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["data"][0]["id"]

def notify_owner(doi, email, status):
    send_email.delay({
        "subject": f"DOI Status Notification: {doi}",
        "recipients": [email],
        "body": f"The DOI {doi} is currently in '{status}' state."
    })
    logger.warning(f"[DOI Polling Task] Email dispatched to {email}")


# === Task registration ===

from celery import shared_task

@shared_task(bind=True, max_retries=5, default_retry_delay=1, name="ultraviolet.poll_doi_until_registered")
def poll_doi_until_registered(self, recid):
    with current_app.app_context():
        logger.warning(f"[DOI Polling Task] Starting poll for recid={recid}")

        try:
            record_dict = fetch_record_dict(recid)
        except PersistentIdentifierError as e:
            logger.warning(f"[DOI Polling Task] PID error for recid={recid}, retrying...")
            raise self.retry(exc=e)

        doi = record_dict.get("pids", {}).get("doi", {}).get("identifier")
        email = extract_owner_email(record_dict)

        if not doi:
            logger.warning(f"[DOI Polling Task] No DOI found for recid={recid}, skipping.")
            return
        if not email:
            logger.warning(f"[DOI Polling Task] No owner email found for recid={recid}, skipping.")
            return

        logger.warning(f"[DOI Polling Task] Found DOI: {doi}, email: {email}")

        try:
            if current_app.config.get("DATACITE_TEST_MODE", False):
                doi = get_random_test_doi()
                logger.warning(f"[DOI Polling Task] Using random test DOI: {doi}")

            status = get_doi_status(doi, test_mode=current_app.config.get("DATACITE_TEST_MODE", False))
            logger.warning(f"[DOI Polling Task] DOI status: {status}")

        except Exception as e:
            logger.warning(f"[DOI Polling Task] Error checking DOI status: {e}, retrying...")
            raise self.retry(exc=e)

        if status not in ["registered", "findable"]:
            logger.warning(f"[DOI Polling Task] DOI status is '{status}', not ready, retrying...")
            raise self.retry(exc=Exception(f"DOI status is '{status}'"))
        else:
            logger.warning(f"[DOI Polling Task] DOI is registered or findable.")
            notify_owner(doi, email, status)
            logger.warning(f"[DOI Polling Task] Notification sent to {email}")



# === Signal hook for postrun ===

@signals.task_postrun.connect
def after_pid_register(sender=None, task_id=None, task=None, args=None, kwargs=None,
                       retval=None, state=None, **other):
    """Trigger DOI polling after register_or_update_pid finishes."""

    if task and task.name == "invenio_rdm_records.services.pids.tasks.register_or_update_pid":
        recid = args[0] if len(args) > 0 else None
        scheme = args[1] if len(args) > 1 else None

        logger.warning(f"[POSTRUN] register_or_update_pid finished: recid={recid}, scheme={scheme}")

        if scheme == "doi" and recid:
            poll_doi_until_registered.delay(recid)
            logger.warning(f"[POSTRUN] DOI polling task queued for recid={recid}")

