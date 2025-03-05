from pydantic import BaseModel, Field,EmailStr
from typing import Optional

class PostOut(BaseModel):
    id: int
    author: str
    title: str = Field(...,max_length=50,min_length=10)

    class config:
        orm_mode = True



class PostCreate(BaseModel):
    author: str
    title: str
    description: str = Field(...,max_length=100,min_length=20)

    class config:
        orm_mode = True



#----------------------
# User Schemas
#----------------------


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str


#----------------------
# Token Schemas
#----------------------


class Login(BaseModel):
    email :str
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None