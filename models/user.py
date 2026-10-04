from sqlalchemy import Column,Integer,String,Text
from database.database import Base

# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password_hash = Column(String,nullable=False)
    role = Column(String,default="user", nullable=False)
