from fastapi import APIRouter, Depends,HTTPException
from pymongo.database import Database
from datetime import datetime
from database import get_db
import database,schemas,oauth2
from bson import ObjectId  # Import ObjectId for MongoDB


router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@router.get("/get_posts",response_model=list[schemas.PostOut])
def get_all_posts(db: Database = Depends(get_db)): 
    collection = db['posts_information']
    show_collection = list(collection.find({}))
    return show_collection




@router.get("/get_post/{post_title}", response_model=schemas.PostOut)
def get_post_by_title(post_title: str, db: Database = Depends(get_db)):
    try:
        post_by_title = db['posts_information'].find_one({'title': post_title})
        
        if not post_by_title:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return post_by_title 
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    

    

@router.post('/create_post',response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Database = Depends(get_db),current_user: dict = Depends(oauth2.get_current_user)):
    try:
        post_dict = post.dict()
        post_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post_dict['user_id'] = str(current_user['_id'])

        result = db['posts_information'].insert_one(post_dict)
        
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Post creation failed")

        # Include the inserted ID in the response
        post_dict["id"] = str(result.inserted_id)  # MongoDB ID is ObjectId, convert to string

        return post_dict  

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



    
@router.delete('/delete/{post_title}')
def delete_post(post_title:str,db: Database = Depends(get_db)):
    get_post = db['post_information'].delete_one({'title':post_title})
    if get_post.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Post deleted successfully"}