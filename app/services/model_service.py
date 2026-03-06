import os
import numpy as np
import random
from app.services.image_service import load_and_preprocess_image

# Hide CUDA errors by disabling GPU visible devices immediately
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

MODEL_PATH = "model/brain_tumor_model.h5"

_MODEL = None
_MODEL_LOADED = False

def get_model():
    global _MODEL, _MODEL_LOADED
    if _MODEL_LOADED:
        return _MODEL
        
    _MODEL_LOADED = True
    print("Lazy loading TensorFlow and the Keras model...")
    try:
        from tensorflow.keras.models import load_model
        if os.path.exists(MODEL_PATH):
            _MODEL = load_model(MODEL_PATH)
            print("Model successfully loaded!")
        else:
            print(f"Warning: Model not found at {MODEL_PATH}.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        
    return _MODEL


def predict_image(file_path: str) -> tuple[str, float]:
    """
    Process image and predict tumor presence.
    Returns a tuple: (prediction: str, confidence: float)
    """
    model = get_model()
    if model is None:
        raise RuntimeError("Machine Learning Model is not loaded. Cannot predict.")

    # 1. Preprocess
    image_data = load_and_preprocess_image(file_path)
    
    # Needs to match input shape (1, 224, 224, 3)
    input_batch = np.expand_dims(image_data, axis=0)
    
    # 2. Predict
    prediction_prob = model.predict(input_batch)[0][0]
    
    # 3. Interpret
    if prediction_prob >= 0.5:
        prediction_label = "Tumor"
        confidence = float(prediction_prob)
    else:
        prediction_label = "No Tumor"
        confidence = float(1.0 - prediction_prob) # Confidence in the "No Tumor" class
        
    return prediction_label, round(confidence, 4)
