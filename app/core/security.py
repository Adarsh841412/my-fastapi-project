import hashlib
from passlib.context import CryptContext

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