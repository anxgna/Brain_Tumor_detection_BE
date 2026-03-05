from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    scans = relationship("MRIScan", back_populates="owner")


class MRIScan(Base):
    __tablename__ = "mri_scans"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="scans")
    prediction = relationship("Prediction", back_populates="scan", uselist=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("mri_scans.id"))
    prediction = Column(String(50))
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    scan = relationship("MRIScan", back_populates="prediction")
