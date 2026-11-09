from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List 
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import (
    UserCreate,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
    GetUser,
)
from app.db.session import get_db
from app.models import User
from app.api.deps import get_current_user, get_current_admin
from app.crud.user import (
    create_user,
    get_users,
    login_user,
    refresh_access_token,
)

router = APIRouter(prefix="/auth", tags=['Authentication'])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user 


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    tokens = login_user(data.username, data.password, db)
    return tokens


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_access_token(payload.refresh_token, db)


@router.get("/get-all-users", response_model=List[GetUser], status_code=status.HTTP_200_OK)
async def users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    all_users = get_users(db)
    return all_users 


