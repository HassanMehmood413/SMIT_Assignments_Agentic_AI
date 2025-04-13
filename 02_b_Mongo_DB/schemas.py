from pydantic import BaseModel, Field, validator,EmailStr
from datetime import datetime



class Post(BaseModel):
    id: str  # ✅ MongoDB _id will be stored as a string
    title: str
    authur: str
    content: str
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_id:str



class PostCreate(BaseModel):
    title: str
    authur: str
    content: str = Field(..., example="This is the content of the post")


    @validator("content")
    def check_content(cls, value):
        char_count = len(value)  # Character count
        if char_count < 20 or char_count > 1000:  # ✅ Ensuring length in characters
            raise ValueError("Content must be between 20 and 1000 characters.")
        return value




class PostOut(BaseModel):
    # id: str  # ✅ Add this to store the MongoDB ObjectId as a string
    title: str
    authur: str
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_id:str


# ----------------
# Users Schemas
# ----------------

class User(BaseModel):
    id: str
    name: str
    password:str
    email:EmailStr
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class UserCreate(BaseModel):
    name:str
    password:str
    email:EmailStr

class UserOut(BaseModel):
    name:str
    email:str
    created_at:str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




# ----------------
# Token Schemas
# ----------------


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str  # Ensure this exists!
    username: str | None = None