import hashlib
from passlib.context import CryptContext
from typing import Union, Any
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import jwt 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def secure_pwd(raw_password: str) -> str:
    # SHA-256 converts the password into a fixed-length 64-character hex string
    password_hash = hashlib.sha256(raw_password.encode("utf-8")).hexdigest()

    # bcrypt receives the 64-character string, not the original password
    return pwd_context.hash(password_hash)

def verify_pwd(raw_password: str, stored_hash: str) -> bool:
    # Apply the same SHA-256 step before checking against the stored bcrypt hash
    password_hash = hashlib.sha256(raw_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(password_hash, stored_hash)


# * JWT implementation 


def create_access_token(subject: Union[str, Any], id: int, expires_delta: Union[timedelta, int, None] = None) -> str:
    if isinstance(expires_delta, int):
        delta = timedelta(minutes=expires_delta)
    elif isinstance(expires_delta, timedelta):
        delta = expires_delta
    else:
        delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + delta
    to_encode = {"exp": expire, "sub": str(subject), "id": id, "type": "access"}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(subject: Union[str, Any], id: int, expires_delta: Union[timedelta, int, None] = None) -> str:
    if isinstance(expires_delta, int):
        delta = timedelta(minutes=expires_delta)
    elif isinstance(expires_delta, timedelta):
        delta = expires_delta
    else:
        delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + delta
    to_encode = {"exp": expire, "sub": str(subject), "id": id, "type": "refresh"}
    return jwt.encode(to_encode, settings.refresh_secret_key, algorithm=settings.algorithm) 






# https://www.freecodecamp.org/news/how-to-add-jwt-authentication-in-fastapi/