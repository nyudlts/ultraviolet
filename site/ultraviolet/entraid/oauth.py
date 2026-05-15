import jwt
from flask import current_app, redirect, request, session
from flask_login import login_user
from invenio_accounts.errors import AlreadyLinkedError
from invenio_accounts.models import UserIdentity


def _email_to_username(email: str) -> str:
    email = email.strip().lower()

    local_part, domain = email.split("@", 1)
    domain_label = domain.split(".", 1)[0]
    email = f"{domain_label}-{local_part}"

    return email[:64]


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

    email = claims.get("email", None)
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

        user.username = _email_to_username(email)
        user.preferences = {
            "visibility": "public",
            "email_visibility": "public",
        }
        user.user_profile = {
            "full_name": claims.get("name", None),
            "affiliations": "New York University",
        }

        datastore.db.session.add(user)

        role = datastore.find_role("nyuusers")
        if role is not None:
            datastore.add_role_to_user(user, role)
        else:
            current_app.logger.warning(
                'Role "nyuusers" does not exist; user was created without it.'
            )

        datastore.commit()

    try:
        UserIdentity.create(user, "entra_id", claims.get("oid"))
    except AlreadyLinkedError as e:
        current_app.logger.warning(f"User {user.id} already linked with Entra ID: {e}")

    login_user(user, remember=True)

    next_url = session.pop("oauth_next", None) or request.args.get("next") or "/"
    return redirect(next_url)
