from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models,schemas
from utils.oauth2 import get_current_user


def all_posts_show(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts



def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)  # ✅ Fix here
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    create = models.Posts(**post.dict(), user_id=current_user.id)  # ✅ Now, user_id is correctly set
    db.add(create)
    db.commit()
    db.refresh(create)
    return create


def update_post_by_id(post: schemas.PostCreate,id:int,db: Session = Depends(get_db)):
    
    fetch_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")

    try:
        for key,value in post.dict().items():
            setattr(fetch_post,key,value)

        db.commit()
        db.refresh(fetch_post)
        return fetch_post
    except Exception as e:
        print("Error",e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Post not Made")
    
    
def delete_post_by_id(id:int,db: Session = Depends(get_db)):
    fetch_post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
    
    db.delete(fetch_post)
    db.commit()
    return {'Message':'Post Deleted Successfully'}

