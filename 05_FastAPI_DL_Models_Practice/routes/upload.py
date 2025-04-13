from fastapi import APIRouter, UploadFile, File
import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

router = APIRouter(tags=['Upload'])

# Global model variable
model = None
IMG_SIZE = (150, 150)

# Upload folder
UPLOADED_FOLDER = r'.\FileUpload\Uploads'
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

# Load model on startup via helper
def load_dl_model():
    global model
    model_path = os.path.join('model', 'cat_dog_model.h5')
    model = load_model(model_path)
    print("✅ Model loaded")


@router.on_event("startup")
def startup_event():
    load_dl_model()


@router.post('/upload')
def upload_files(file: UploadFile = File(...)):
    global model

    # Save file
    file_path = os.path.join(UPLOADED_FOLDER, file.filename)
    with open(file_path, 'wb+') as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Preprocess the image
    img = image.load_img(file_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # normalize

    # Predict
    prediction = model.predict(img_array)[0][0]

    # You can set a threshold, e.g. 0.5 for binary classification
    result = "Dog" if prediction > 0.5 else "Cat"

    return {
        "filename": file.filename,
        "prediction": result,
        "confidence": float(prediction)
    }
