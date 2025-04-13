from fastapi import APIRouter,Depends,HTTPException
from pymongo.database import Database
from datetime import datetime
from database import get_db
import hashing
import schemas


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/',response_model=list[schemas.UserOut])
def get_users(db:Database = Depends(get_db)):
    all_users = db['users_accounts_information']
    collection = list(all_users.find({}))
    return collection


@router.post('/create_user',response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db:Database = Depends(get_db)):
    try:
        
        post_user = user.dict()
        find_user = db['users_accounts_information'].find_one({'email':post_user['email']})
        if find_user:
            raise HTTPException(status_code=500,detail='user already exists')
        
        post_user['password'] = hashing.get_password_hash(user.password)
        post_user["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = db['users_accounts_information'].insert_one(post_user)

        if not result.inserted_id:
            raise HTTPException(status_code=500,detail='post creation failed')
        post_user['id'] = str(result.inserted_id)

        return post_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

