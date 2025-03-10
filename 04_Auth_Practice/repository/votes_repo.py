from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user
import schemas,models




def give_new_vote(vote: schemas.Votes,db:Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    find_post = db.query(models.User).filter(models.Posts.id == vote.post_id).first()

    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post Not Found')
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id).first()

    if(vote.direction == 1):
        if vote_query:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='You Already Voted for this post')
        
        else:
            new_vote = models.Votes(user_id = current_user.id , post_id = vote.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {'message':'Vote created successfully'}
        

    elif (vote.direction == 0):
        if not vote_query:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have not voted for this post")
        else:
            db.delete(vote_query)
            db.commit()
            return {"message": "Vote deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote direction")

