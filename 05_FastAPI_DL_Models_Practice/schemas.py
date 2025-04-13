from pydantic import BaseModel ,EmailStr,validator
from typing import List



class User(BaseModel):
    id : int
    name:str
    email:str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

    @validator('password')
    def validate_password(cls,v):
        if not len(v)>=8:
            raise ValueError('Password must be at least 8 characters long')
        return v

