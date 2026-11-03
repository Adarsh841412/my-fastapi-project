from pydantic import BaseModel ,EmailStr , Field
from typing import Annotated
from datetime import datetime
from enum import Enum 


class Role(str,Enum):
    admin = "admin"
    user = "user"



class UserBase(BaseModel):
     name:str 
     email:EmailStr 

class UserCreate(UserBase):

    password:Annotated[str,Field(min_length=8,max_length=30)]




class UserResponse(UserBase):
        id:int 
        role:Role = Role.user 
        is_verified:bool 
        is_active:bool 
        created_at:datetime 
        updated_at:datetime  


        class Config:
             from_attributes = True # when you fetch data from db this will tell instead of thing like dictanly that pydantic do , thin its a object 



class LoginUser(BaseModel):
     email:EmailStr 
     password:Annotated[str,Field(min_length=8,max_length=25)]

     class Config:
          from_attributes=True 


class GetUser(BaseModel):
     email:EmailStr 
     role:Role

     class Config:
          from_attributes=True 
          use_enum_values=True 
          