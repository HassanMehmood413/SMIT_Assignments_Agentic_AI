from fastapi import HTTPException,Depends,status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
import schemas,database,models
from dotenv import load_dotenv
from typing import Annotated
import jwt
import os

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))



def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str,credential_exception:HTTPException):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get('sub')

        if not user_id or not user_id.isdigit():
            raise credential_exception
        
        return schemas.TokenData(id=int(user_id))
    
    except:
        raise credential_exception



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not Validate credentials',
        headers={'WWW-Authenticate': "Bearer"}
    )

    token_data = verify_token(token, credential_exception)

    print(token_data)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    print("✅ Authenticated User in get_current_user:", user)  # Debugging Output

    if user is None:
        raise credential_exception
    
    return user
