from sqlalchemy import Column,String,Text,DateTime,Integer
from datetime import datetime
from pydantic import EmailStr
from database import Base


class Posts(Base):
    __tablename__ = 'Posts'

    id = Column(Integer,primary_key=True,index=True)
    author = Column(String,nullable=False)
    title = Column(String,nullable=False)
    description = Column(Text,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)