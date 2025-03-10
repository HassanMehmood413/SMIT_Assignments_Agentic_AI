from pydantic import BaseModel, Field,EmailStr,validator
from typing import Optional, List
import re

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
    password: str = Field(
        ...,
        
        description="Password must be at least 8 characters long and include at least one letter and one number."
    )

    @validator('password')
    def password_complexity(cls, v):
        # Use Python's re module with look-ahead assertions.
        pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        if not pattern.match(v):
            raise ValueError("Password must be at least 8 characters long and include at least one letter and one number.")
        return v


class UserOut(BaseModel):
    id: int
    email: str
    posts : List[PostOut]


    class Config:
        orm_mode = True


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



#----------------------
# Votes Schemas
#----------------------
class Votes(BaseModel):
    direction:int =  Field(...,le=1,ge=0)
    post_id: int



#----------------------
# Messages Schemas
#----------------------

class Messages(BaseModel):
    direction:int =  Field(...,le=1,ge=0)
    post_id: int
    message: str