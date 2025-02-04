from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import UploadedFile
from datetime import datetime
from database import get_db
import models
import os

UPLOAD_FOLDER = r'.\02_Exceptions,folder_structure\Uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

app.mount('/static', StaticFiles(directory=UPLOAD_FOLDER), name='static')

MAX_FILE_SIZE = 10 * 1024 * 1024  


@app.post('/uploads')
async def upload_files(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await file.read()
    file_size = len(file_content)
    Allowed_extensions = ['txt', 'png', 'jpeg']
    ext = file.filename.split('.')[-1].lower()

    if ext not in Allowed_extensions:
        raise HTTPException(status_code=415, detail="File extension not allowed")

    await file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size is too large")
        
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, 'wb') as buffer:
        buffer.write(file_content)

    file_url = f'/static/{file.filename}'

    db_file = UploadedFile(
        filename=file.filename,
        file_content=file_content,
        uploaded_at=datetime.utcnow()
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return {'file_name': file.filename, 'file_path': file_url}



@app.get('/get/{file_id}')
async def get_file_content(file_id: int, db: Session = Depends(get_db)):
    file = db.query(models.UploadedFile).filter(UploadedFile.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    print(f"File Content (Binary): {file.file_content[:20]}...")  

    try:
        content = file.file_content.decode('utf-8')  
    except UnicodeDecodeError:
        raise HTTPException(status_code=415, detail="File is not a text-based file")
    
    return {"filename": file.filename, "file_content": content}


@app.delete('/delete/{file_name}')
async def delete_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)

    return {"message": f"File '{file_name}' deleted successfully"}
