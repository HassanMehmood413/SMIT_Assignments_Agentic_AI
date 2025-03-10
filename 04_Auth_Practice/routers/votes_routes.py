from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user
from repository import votes_repo
import schemas,models


router = APIRouter(
    tags=['Votes'],
    prefix='/votes'
)


@router.post('/create_vote')
def give_vote(vote: schemas.Votes,db:Session = Depends(get_db),current_user: int = Depends(get_current_user)):
    return votes_repo.give_new_vote(vote,db,current_user)