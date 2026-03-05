import numpy as np
import random
from app.services.image_service import load_and_preprocess_image

import os
from tensorflow.keras.models import load_model

MODEL_PATH = "model/brain_tumor_model.h5"

# Load model globally to avoid loading on every request
if os.path.exists(MODEL_PATH):
    _MODEL = load_model(MODEL_PATH)
else:
    _MODEL = None
    print(f"Warning: Model not found at {MODEL_PATH}. Prediction will fail.")


def predict_image(file_path: str) -> tuple[str, float]:
    """
    Process image and predict tumor presence.
    Returns a tuple: (prediction: str, confidence: float)
    """
    if _MODEL is None:
        raise RuntimeError("Machine Learning Model is not loaded. Cannot predict.")

    # 1. Preprocess
    image_data = load_and_preprocess_image(file_path)
    
    # Needs to match input shape (1, 224, 224, 3)
    input_batch = np.expand_dims(image_data, axis=0)
    
    # 2. Predict
    prediction_prob = _MODEL.predict(input_batch)[0][0]
    
    # 3. Interpret
    if prediction_prob >= 0.5:
        prediction_label = "Tumor"
        confidence = float(prediction_prob)
    else:
        prediction_label = "No Tumor"
        confidence = float(1.0 - prediction_prob) # Confidence in the "No Tumor" class
        
    return prediction_label, round(confidence, 4)
