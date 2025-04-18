from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models,schemas
from utils.oauth2 import get_current_user
import hashing




def show_all_user(db:Session = Depends(get_db),get_user: int = Depends(get_current_user)):
    try:
        fetch_all_users = db.query(models.User).all()
        return fetch_all_users
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='400 BaD request')


def user_new_create(user: schemas.UserCreate,db:Session = Depends(get_db)):
    try:
        hashed_password = hashing.hash_password(user.password)
        user.password = hashed_password
        create_new_user = models.User(**user.dict())
        db.add(create_new_user)
        db.commit()
        db.refresh(create_new_user)
        return create_new_user
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Error Occuring')
    