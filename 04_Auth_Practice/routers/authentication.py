from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from utils import oauth2
from sqlalchemy.orm import Session
import schemas,database,models
from hashing import verify_password


router = APIRouter()

@router.post('/login',response_model=schemas.Token)
def login(request : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Crendentials",
        )
    
    if not verify_password(request.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Crendentials",
        )
    
    access_token = oauth2.create_access_token(data={'sub': str(user.id)})

    return {'access_token':access_token,"token_type":"bearer"}
