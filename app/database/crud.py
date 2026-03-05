from sqlalchemy.orm import Session
from app.database import models
from app.schemas import request_schema

# --- User CRUD ---

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: request_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, password_hash=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Scan CRUD ---

def create_scan(db: Session, file_path: str, user_id: int = None):
    db_scan = models.MRIScan(file_path=file_path, user_id=user_id)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def get_scan(db: Session, scan_id: int):
    return db.query(models.MRIScan).filter(models.MRIScan.id == scan_id).first()

def get_scans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MRIScan).offset(skip).limit(limit).all()

# --- Prediction CRUD ---

def create_prediction(db: Session, scan_id: int, prediction: str, confidence: float):
    db_prediction = models.Prediction(
        scan_id=scan_id, prediction=prediction, confidence=confidence
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction
