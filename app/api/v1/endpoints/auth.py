from fastapi import APIRouter ,Depends,HTTPException,status 
from app.schemas import UserCreate,UserResponse
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.crud.user import create_user
router = APIRouter(prefix="/auth",tags=['Authentication'])



@router.post("/signup", response_model=UserResponse , status_code=status.HTTP_201_CREATED)
def signup(user:UserCreate, db:Session=Depends(get_db)):

    # * check first that user not exist 

    # * create user 

    new_user = create_user(db,user)
    return new_user 


