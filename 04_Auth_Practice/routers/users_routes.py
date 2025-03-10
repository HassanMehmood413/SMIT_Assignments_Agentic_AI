from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models,schemas
from repository import user_repo
from utils.oauth2 import get_current_user
import hashing


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get('/',response_model=List[schemas.UserOut])
def show_user(db:Session = Depends(get_db),get_user: int = Depends(get_current_user)):
    return user_repo.show_all_user(db,get_user)


@router.post('/create_user',response_model=schemas.UserOut)
def user_create(user: schemas.UserCreate,db:Session = Depends(get_db)):
    return user_repo.user_new_create(user,db)
    