from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
import oauth2
from bson import ObjectId
from hashing import verify_password

router = APIRouter()

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_db)):
    user = db['users_accounts_information'].find_one({'email': request.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(request.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Corrected: Convert ObjectId to string
    access_token = oauth2.create_access_token(data={"sub": str(user['_id'])})

    return {"access_token": access_token, "token_type": "bearer"}
