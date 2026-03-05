import cv2
import numpy as np


def resize_image(image: np.ndarray, size: tuple = (224, 224)) -> np.ndarray:
    """Resize image to the target size."""
    return cv2.resize(image, size)

def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normalize image pixel values to [0, 1]."""
    return image / 255.0
