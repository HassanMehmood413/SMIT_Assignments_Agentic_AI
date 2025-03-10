from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user
from repository import votes_repo
import schemas,models


router = APIRouter(
    tags=['Message'],
    prefix='/message'
)


@router.post('/give_message')
def give_message(message: schemas.Messages,db:Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    find_post = db.query(models.User).filter(models.Posts.id == message.post_id).first()

    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post Not Found')
    
    message_query = db.query(models.Messages).filter(models.Messages.post_id == message.post_id,models.Messages.user_id == current_user.id).first()

    if(message.direction == 1):
        if message_query:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='You Already Commented for this post')
        
        else:
            new_message = models.Messages(post_id=message.post_id,user_id = current_user.id,message=message.message)
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            return {'Message':'Message successfull'}
    
    elif message.direction == 0:
        if not new_message:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have not voted for this post")
        else:
            db.delete(new_message)
            db.commit()
            return {"message": "Vote deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote direction")

    