from sqlalchemy.orm import Session
from sqlalchemy import select 
from app.models import User, Token
from pydantic import EmailStr
from app.schemas import UserCreate
from app.core import secure_pwd, verify_pwd
from app.Exceptions.auth_exceptions import InvalidCredentialException, EmailAlreadyExistException
from app.core.security import create_access_token, create_refresh_token 
from app.core.config import settings 
import jwt 


def get_users(db: Session):
    stmt = select(User)
    return db.scalars(stmt).all() 


def create_user(db: Session, user: UserCreate):
    stmt = select(User).where(User.email == user.email)
    existing_user = db.scalars(stmt).first()
    if existing_user:
        raise EmailAlreadyExistException("This email is already registered. Please login or use a different email.")

    new_user = User(
        name=user.name,
        email=user.email,
        password=secure_pwd(raw_password=user.password),
    )
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user 


def get_token(db: Session, token: str):
    query = select(Token).where(Token.token == token)
    return db.scalars(query).first() 


def create_token(db: Session, token: str, user_id: int):
    db_token = Token(token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def login_user(email: EmailStr, password: str, db: Session):
    stmt = select(User).where(User.email == email)
    user = db.scalar(stmt)

    if not user or not verify_pwd(password, user.password):
        raise InvalidCredentialException("Incorrect email or password")

    if not user.is_active:
        raise InvalidCredentialException("Account is currently inactive")

    return {
        'access_token': create_access_token(user.email, user.id),
        'refresh_token': create_refresh_token(user.email, user.id),
        'token_type': 'bearer',
    }


def refresh_access_token(refresh_token: str, db: Session):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.refresh_secret_key,
            algorithms=[settings.algorithm]
        )
        token_type = payload.get("type")
        if token_type != "refresh":
            raise InvalidCredentialException("Invalid token type")

        user_id = payload.get("id")
        user_email = payload.get("sub")
        if not user_id or not user_email:
            raise InvalidCredentialException("Invalid token payload")

    except jwt.PyJWTError:
        raise InvalidCredentialException("Invalid or expired refresh token")

    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise InvalidCredentialException("User not found or inactive")

    return {
        'access_token': create_access_token(user.email, user.id),
        'refresh_token': create_refresh_token(user.email, user.id),
        'token_type': 'bearer',
    }
    
    

