from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from typing import List
from repository import post_repo
from database import get_db
from utils.oauth2 import get_current_user
import models,schemas


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/',response_model=List[schemas.PostOut])
def all_posts(db: Session = Depends(get_db)):
    return post_repo.all_posts_show(db)



@router.post('/create',response_model=schemas.PostOut)
def createpost(post: schemas.PostCreate,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return post_repo.create_post(post,db,current_user)
    


@router.put('/update_post/{id}')
def update_post(post: schemas.PostCreate,id:int,db: Session = Depends(get_db)):
    return post_repo.update_post_by_id(post,id,db)
    

@router.delete('/delete_post/{id}')
def delete_post(id:int,db: Session = Depends(get_db)):
    return post_repo.delete_post_by_id(id,db)


