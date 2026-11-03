from sqlalchemy.orm import Session
from sqlalchemy import select 
from app.models import User ,Token
from pydantic import EmailStr
from app.schemas import UserCreate
from app.core import secure_pwd 


def get_users(db:Session,email:EmailStr):

    stmt = select(User)
    users = db.scalars(stmt).all() 
    return users 


def create_user(db:Session,user:UserCreate):
    user = User(
        name=user.name ,
        email=user.email ,
        password=secure_pwd(raw_password=user.password),
    )
    db.add(user)
    db.commit() 
    db.refresh(user)
    return user 


def get_token(db:Session,token:str):
    query = select(Token).where(Token.token ==  token)
    tkn = db.scalars(query).first() 
    return tkn 


def create_token(db: Session, token: str, user_id: int):
    db_token = Token(token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token