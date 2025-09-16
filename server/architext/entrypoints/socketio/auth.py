from dataclasses import dataclass
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers.verifytoken import VerifyTokenOptions, verify_token
from architext.entrypoints.socketio.settings import CLERK_SECRET_KEY


def user_id_from_clerk_token(token: str) -> str:
    res = verify_token(token, VerifyTokenOptions(
        secret_key=CLERK_SECRET_KEY
    ))  # add jwt_key to make it networkless
    user_id = res['sub']
    return user_id


@dataclass
class ClerkUserDetails():
    id: str
    username: str
    email: str


def get_clerk_user_details(user_id: str) -> ClerkUserDetails:
    with Clerk(
        bearer_auth=CLERK_SECRET_KEY,
    ) as clerk:
        res = clerk.users.get(user_id=user_id)
        mail_res = clerk.email_addresses.get(email_address_id=res and res.primary_email_address_id or "")
        return ClerkUserDetails(
            id=user_id,
            username=res and res.username or "",
            email=mail_res and mail_res.email_address or ""
        )