from fastapi import FastAPI, status, Depends,HTTPException,staticfiles
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db,Base,engine
import schemas,model
from routes import user,upload


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="./FileUpload/Uploads"), name="static")


Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(upload.router)
