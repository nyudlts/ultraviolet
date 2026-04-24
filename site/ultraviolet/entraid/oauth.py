import re
from collections.abc import Mapping

import jwt
import requests
from flask import current_app, redirect, request, session
from flask_login import login_user


def _first_present(data, *keys, default=None):
    for key in keys:
        value = data.get(key)
        if value:
            return value
    return default


def _as_profile_dict(value):
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _sanitize_username(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_-]", "_", value)
    value = re.sub(r"^[^a-z]+", "u_", value)
    value = re.sub(r"_+", "_", value)
    if len(value) < 3:
        value = f"u_{value}".ljust(3, "0")
    return value[:64]


def _extract_profile_from_id_token(token):
    token = _as_profile_dict(token)
    if not token:
        return {}

    id_token = token.get("id_token")
    if not id_token:
        return {}

    try:
        if isinstance(id_token, bytes):
            id_token = id_token.decode("utf-8")

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


def _extract_profile_from_graph(token):
    token = _as_profile_dict(token)
    access_token = token.get("access_token")
    if not access_token:
        return {}

    if isinstance(access_token, bytes):
        access_token = access_token.decode("utf-8")

    try:
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json() or {}
    except Exception:
        current_app.logger.exception(
            "Failed to fetch Entra profile from Microsoft Graph"
        )
        return {}


def entra_authorized_handler(token, remote, response=None):
    """
    Custom authorized handler for Microsoft Entra ID.
    """
    claims = _extract_profile_from_id_token(token)
    if not claims:
        claims = _as_profile_dict(response)
    if not claims:
        claims = _extract_profile_from_graph(token)
    if not claims:
        try:
            if hasattr(remote, "userinfo") and callable(remote.userinfo):
                claims = remote.userinfo() or {}
        except Exception:
            current_app.logger.exception("Failed to fetch Entra userinfo")

    claims = _as_profile_dict(claims)

    entraid = _first_present(claims, "oid", "sub", default=None)
    email = _first_present(
        claims,
        "email",
        "preferred_username",
        "upn",
        "unique_name",
        default=None,
    )
    given_name = _first_present(claims, "given_name", default="")
    family_name = _first_present(claims, "family_name", default="")
    display_name = _first_present(claims, "name", default="")

    if not entraid and not email:
        raise ValueError(
            "Microsoft Entra login did not provide usable claims. "
            "Expected oid/sub or an email-like identifier."
        )

    datastore = current_app.extensions["security"].datastore
    lookup_email = email or f"{entraid}@entra.local"

    user = datastore.find_user(email=lookup_email)

    if user is None:
        user = datastore.create_user(
            email=lookup_email,
            active=True,
            confirmed_at=None,
        )

        if hasattr(user, "username"):
            base_username = email or display_name or lookup_email
            user.username = _sanitize_username(base_username)

        if hasattr(user, "first_name"):
            user.first_name = given_name or display_name
        if hasattr(user, "last_name"):
            user.last_name = family_name

        datastore.db.session.add(user)
        datastore.commit()

    login_user(user, remember=True)

    next_url = session.pop("oauth_next", None) or request.args.get("next") or "/"
    return redirect(next_url)
