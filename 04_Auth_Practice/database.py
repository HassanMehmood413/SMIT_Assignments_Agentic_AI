from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv('DB_URL')

engine = create_engine(DB_URL)

sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()