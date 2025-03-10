from sqlalchemy import Column,String,Text,DateTime,Integer,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from database import Base


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,index=True)
    author = Column(String,nullable=False)
    title = Column(String,nullable=False)
    description = Column(Text,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # ✅ `users.id`

    owner = relationship('User',back_populates='posts')



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)

    posts = relationship('Posts', back_populates='owner', cascade="all, delete")  # ✅ Fix relationship



class Votes(Base):
    __tablename__ = 'votes'

    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADe'),primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)


class Messages(Base):
    __tablename__ = 'messaeges'


    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADe'),primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
    message = Column(Text,nullable=False)