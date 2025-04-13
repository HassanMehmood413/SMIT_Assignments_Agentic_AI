from fastapi import APIRouter, status, Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db,Base,engine
import schemas,model



router = APIRouter(
    tags=['Users']
)




@router.get("/show_users")
def get_all_users(db:Session = Depends(get_db)):
    all_users = db.query(model.User).all()
    return {"Users":all_users}


@router.post("/create_user",response_model=schemas.User)
def create_user(User:schemas.UserCreate,db:Session = Depends(get_db)):
    new_user = model.User(**User.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user



@router.put("/update_user/{id}")
def update_user(id:int,User:schemas.UserCreate,db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id ==id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    for key,value in User.dict().items():
        setattr(user,key,value)

    db.commit()
    db.refresh(user)
    return {"User":user}



@router.delete('/delete_user/{id}')
def delete_user(id:int,User:schemas.UserCreate,db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(user)
    db.commit()
    return {"Deleted Successfully"}



