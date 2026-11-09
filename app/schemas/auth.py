from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from datetime import datetime
from enum import Enum 


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    name: str 
    email: EmailStr 


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=128)]


class UserResponse(UserBase):
    id: int 
    role: Role = Role.user 
    is_verified: bool 
    is_active: bool 
    created_at: datetime 
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class LoginUser(BaseModel):
    email: EmailStr 
    password: Annotated[str, Field(min_length=8, max_length=128)]

    model_config = ConfigDict(from_attributes=True) 


class GetUser(BaseModel):
     email:EmailStr 
     role:Role
     name:str 

     model_config = {
          "from_attributes": True,
          "use_enum_values": True
     }



class TokenSchema(BaseModel):
     exp:int
     sub:str
     id:int
     type:str | None = None


class TokenResponse(BaseModel):
     access_token: str
     refresh_token: str
     token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
     refresh_token: str
          