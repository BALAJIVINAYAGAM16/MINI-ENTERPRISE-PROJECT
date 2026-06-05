from datetime import datetime, timedelta, timezone
import hashlib
import secrets

import bcrypt
from jose import JWTError, jwt

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

# bcrypt limitation
BCRYPT_MAX_PASSWORD_BYTES = 72


def is_valid_bcrypt_password(password: str) -> bool:
    return len(password.encode("utf-8")) <= BCRYPT_MAX_PASSWORD_BYTES


# ==========================
# Password Functions
# ==========================

def hash_password(password: str) -> str:
    if not is_valid_bcrypt_password(password):
        raise ValueError(
            "Password cannot be longer than 72 bytes"
        )

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    if not is_valid_bcrypt_password(password):
        return False

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except (TypeError, ValueError):
        return False


# ==========================
# JWT Access Token
# ==========================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access"
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        return None


# ==========================
# Refresh Token
# ==========================

def create_refresh_token() -> tuple[str, datetime]:

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    token = secrets.token_urlsafe(48)

    return token, expires_at.replace(
        tzinfo=None
    )


# ==========================
# Password Reset Token
# ==========================

def create_password_reset_token(
    expires_minutes: int = 30
) -> tuple[str, datetime]:

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(minutes=expires_minutes)
    )

    token = secrets.token_urlsafe(32)

    return token, expires_at.replace(
        tzinfo=None
    )


# ==========================
# Token Hashing
# ==========================

def hash_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()