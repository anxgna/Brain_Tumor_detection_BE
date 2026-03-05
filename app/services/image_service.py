import os
from fastapi import UploadFile
import cv2
import numpy as np

from app.utils.preprocessing import resize_image, normalize_image


async def process_upload_file(file: UploadFile, uploads_dir: str = "uploads/") -> str:
    """Save the uploaded file and return its path."""
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path


def load_and_preprocess_image(file_path: str) -> np.ndarray:
    """Read image from path, resize it and normalize."""
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"Could not read image from {file_path}")
    
    # Convert from OpenCV's BGR output to the RGB format that Keras loaded during training
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    image = resize_image(image)
    image = normalize_image(image)
    return image
