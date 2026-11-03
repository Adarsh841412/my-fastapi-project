from app.models import Base 
from sqlalchemy.orm import Mapped,MappedColumn
from sqlalchemy import String,Boolean,DateTime,Integer
from datetime import datetime
class User(Base):
    __tablename__='user_account'
    id:Mapped[int] = MappedColumn(primary_key=True)
    name:Mapped[str] = MappedColumn(String(50))
    email:Mapped[str]=MappedColumn(String(255),unique=True , index=True)
    password:Mapped[str] = MappedColumn(String(255),nullable=False)


    # authentication and authorizatino related fields 

    is_verified :Mapped[bool] = MappedColumn(Boolean,default=False)  # verify your otp 
    is_active :Mapped[bool]= MappedColumn(Boolean,default=False) # verify your email 
    role:Mapped[str]= MappedColumn(String(255), default='user')  # # For authorization (user, admin, etc.)

    created_at:Mapped[datetime] = MappedColumn(DateTime , default = datetime.utcnow)
    updated_at : MappedColumn[datetime] = MappedColumn(DateTime, default = datetime.utcnow , onupdate=datetime.utcnow)



class Token(Base):
    __tablename__='tokens'
    id:Mapped[int]=MappedColumn(Integer,primary_key=True)
    token:Mapped[str]=MappedColumn(String(400),index=True)
    user_id:Mapped[int]












