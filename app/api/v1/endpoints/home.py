from fastapi import APIRouter, Depends
from app.api.deps import get_current_user 
from app.models import User

router = APIRouter(tags=['Home page'])


@router.get("/")
def home(current_user: User = Depends(get_current_user)):
    return {
        "message": "Welcome to the home page!",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "role": current_user.role,
        }
    }




