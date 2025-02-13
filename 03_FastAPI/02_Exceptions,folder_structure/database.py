from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine


DBURL = 'postgresql://postgres:CreatePassword123@localhost:5432/hassan'

engine = create_engine(DBURL,echo=True)

session = sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()