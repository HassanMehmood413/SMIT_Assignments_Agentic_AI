from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.types import LargeBinary  
from datetime import datetime
from database import Base

class UploadedFile(Base):
    __tablename__ = 'uploaded_files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_content = Column(LargeBinary) 
    uploaded_at = Column(DateTime, default=datetime.utcnow)
