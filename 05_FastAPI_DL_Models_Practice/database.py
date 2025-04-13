from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_URL="postgresql://neondb_owner:npg_XqoN2csn4TPl@ep-misty-tooth-a579k2ep-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"


engine = create_engine(BASE_URL)

session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()