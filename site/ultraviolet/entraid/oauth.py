import re

from flask import current_app, redirect, request, session
from flask_login import login_user
import jwt


def _sanitize_username(value: str) -> str:
    value = value.strip().lower()

    if "@" in value:
        local_part, domain = value.split("@", 1)
        domain_label = domain.split(".", 1)[0]
        value = f"{domain_label}-{local_part}"

    value = re.sub(r"[^a-z0-9_-]", "-", value)
    value = re.sub(r"^[^a-z]+", "u-", value)
    value = re.sub(r"-+", "-", value).strip("-")

    if len(value) < 3:
        value = f"u-{value}".ljust(3, "0")

    return value[:64]


def _decode_id_token(token):
    id_token = (token or {}).get("id_token")
    if not id_token:
        return {}

    if isinstance(id_token, bytes):
        id_token = id_token.decode("utf-8")

    try:
        return (
            jwt.decode(
                id_token,
                options={
                    "verify_signature": False,
                    "verify_aud": False,
                    "verify_exp": False,
                },
            )
            or {}
        )
    except Exception:
        current_app.logger.exception("Failed to decode Entra id_token")
        return {}


def entra_authorized_handler(token, remote, response=None):
    """Custom authorized handler for Microsoft Entra ID."""
    claims = _decode_id_token(token)

    email = claims.get("email") or claims.get("preferred_username") or claims.get("upn")
    if not email:
        raise ValueError("Microsoft Entra login did not provide an email claim.")

    datastore = current_app.extensions["security"].datastore
    user = datastore.find_user(email=email)

    if user is None:
        user = datastore.create_user(
            email=email,
            active=True,
            confirmed_at=None,
        )

        if hasattr(user, "username"):
            user.username = _sanitize_username(email)

        datastore.db.session.add(user)
        datastore.commit()

    login_user(user, remember=True)

    next_url = session.pop("oauth_next", None) or request.args.get("next") or "/"
    return redirect(next_url)
