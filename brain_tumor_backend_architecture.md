# Brain Tumor Detection System (Backend Architecture)

## 1. Project Overview

The Brain Tumor Detection System is a machine learning powered backend
service designed to classify MRI brain scan images into two
categories: - Tumor Present (Yes) - No Tumor (No)

The backend service is implemented using FastAPI, integrates a deep
learning model for inference, and uses MySQL for storing metadata,
prediction logs, and user information.

------------------------------------------------------------------------

## 2. System Architecture

Client (Frontend) \| \| FastAPI Server \| \|------ Image Preprocessing
Pipeline \| \|------ ML Model Inference Engine \| \|------ MySQL
Database \| \|------ File Storage (MRI Images)

------------------------------------------------------------------------

## 3. Tech Stack

Backend Framework: FastAPI\
ML Framework: TensorFlow / PyTorch\
Image Processing: OpenCV / PIL\
Database: MySQL\
ORM: SQLAlchemy\
Data Validation: Pydantic\
Server: Uvicorn\
Storage: Local filesystem or S3

------------------------------------------------------------------------

## 4. Dataset

Dataset contains MRI images labeled: Yes → Tumor Present\
No → Tumor Absent

Typical dataset structure:

dataset/ train/ yes/ no/ test/ yes/ no/

------------------------------------------------------------------------

## 5. Machine Learning Pipeline

### Data Preprocessing

Steps: 1. Image resizing 2. Normalization 3. Noise reduction 4. Contrast
enhancement 5. Data augmentation

Typical image size: 224 x 224 x 3

------------------------------------------------------------------------

## 6. Model Architecture

A CNN based binary classification model.

Example structure:

Input Layer (224x224x3)

Conv2D → ReLU → MaxPooling\
Conv2D → ReLU → MaxPooling\
Conv2D → ReLU → MaxPooling

Flatten\
Dense (128)\
Dropout

Dense (1) → Sigmoid

Output: 0 → No Tumor\
1 → Tumor

Loss: Binary Cross Entropy\
Optimizer: Adam

Evaluation Metrics: Accuracy, Precision, Recall, F1 Score

------------------------------------------------------------------------

## 7. Backend Folder Structure

brain-tumor-backend/

app/ main.py config.py

    api/
        routes.py
        prediction.py
        health.py

    services/
        model_service.py
        image_service.py

    database/
        database.py
        models.py
        crud.py

    schemas/
        request_schema.py
        response_schema.py

    utils/
        preprocessing.py
        logger.py

model/ brain_tumor_model.h5

uploads/

requirements.txt

------------------------------------------------------------------------

## 8. API Endpoints

Health Check: GET /health

Upload MRI: POST /upload

Prediction: POST /predict

Example Response:

{ "prediction": "Tumor", "confidence": 0.94 }

------------------------------------------------------------------------

## 9. Database Design

Database: brain_tumor_detection

Users Table: id \| email \| password_hash \| created_at

MRI Scans Table: id \| file_path \| uploaded_at \| user_id

Predictions Table: id \| scan_id \| prediction \| confidence \|
created_at

------------------------------------------------------------------------

## 10. Database Connection

mysql+pymysql://username:password@localhost:3306/brain_tumor_detection

Example:

engine = create_engine(DATABASE_URL) SessionLocal =
sessionmaker(bind=engine)

------------------------------------------------------------------------

## 11. File Storage

MRI images stored in:

uploads/

Example: uploads/scan_123.png

Database stores file path reference.

------------------------------------------------------------------------

## 12. End-to-End Workflow

User uploads MRI scan\
→ FastAPI receives request\
→ Image preprocessing\
→ Model inference\
→ Prediction generated\
→ Result stored in MySQL\
→ Response returned to client

------------------------------------------------------------------------

End of Backend Architecture
