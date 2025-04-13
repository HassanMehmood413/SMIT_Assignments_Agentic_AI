from pydantic import BaseModel
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import LargeBinary
from sqlalchemy import Column, Integer, String,DateTime
from datetime import datetime



class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)


class UploadFiles(Base):
    __tablename__ = "upload_files"

    id = Column(Integer,primary_key=True,nullable=False)
    file_name = Column(String,nullable=False,index=True)
    file_content = Column(LargeBinary)
    uploaded_at = Column(DateTime,default=datetime.utcnow)
