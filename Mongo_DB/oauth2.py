from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import schemas, database,oauth2
from pymongo.database import Database
from bson import ObjectId




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token: str, credential_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')

        # Check if user_id exists and is numeric
        if user_id is None or not ObjectId.is_valid(user_id):
            raise credential_exception
    

        return schemas.TokenData(id=user_id)
    except JWTError:
        raise credential_exception
    


def get_current_user(token: str = Depends(oauth2.oauth2_scheme), db: Database = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    # Verify the token and retrieve user data
    token_data = verify_token(token, credentials_exception)
    
    # Fetch the user from the database using the token's user id
    user = db['users_accounts_information'].find_one({'_id':ObjectId(token_data.id)})
    
    if user is None:
        raise credentials_exception
    
    return user  # Return the user object directly, not a Depends object
