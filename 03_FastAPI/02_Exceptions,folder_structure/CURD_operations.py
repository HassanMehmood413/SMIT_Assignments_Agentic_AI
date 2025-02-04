
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil

UPLOAD_FOLDER = r'.\02_Exceptions,folder_structure\Uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = FastAPI()

app.mount('/static', StaticFiles(directory=UPLOAD_FOLDER), name='static')

@app.post('/uploads')
async def upload_files(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)  

    file_url = f'/static/{file.filename}'

    return {'file_name': file.filename, 'file_path': file_url}



@app.delete('/delete/{file_name}')
async def delete_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Remove the file from the folder
    os.remove(file_path)

    return {"message": f"File '{file_name}' deleted successfully"}
