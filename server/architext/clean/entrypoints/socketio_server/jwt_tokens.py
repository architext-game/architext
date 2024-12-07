import os
import jwt
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

# Secret key and JWT settings
SECRET_KEY = "patatasfritas"
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRY = {"hours": 1}
REFRESH_TOKEN_EXPIRY = {"days": 7}

def generate_jwt(is_refresh=False, **fields):
    """
    Generate a JWT. Use `is_refresh=True` to generate a refresh token.
    """
    expiry = REFRESH_TOKEN_EXPIRY if is_refresh else ACCESS_TOKEN_EXPIRY
    payload = {
        **fields,
        "exp": datetime.now(timezone.utc) + timedelta(**expiry),
        "is_refresh": is_refresh  # Flag to indicate token type
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str):
    """
    Decode and validate a JWT.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def refresh_token(refresh_token):
    """
    Validate a refresh token and generate a new access token.
    """
    try:
        payload = decode_jwt(refresh_token)
        if not payload.get("is_refresh"):
            raise ValueError("Provided token is not a refresh token")
        
        # Generate a new access token using data from the refresh token
        new_access_token = generate_jwt(
            is_refresh=False,
            user_id=payload["user_id"],
            username=payload["username"]
        )
        return new_access_token
    except ValueError as e:
        raise ValueError(f"Could not refresh token: {str(e)}")
