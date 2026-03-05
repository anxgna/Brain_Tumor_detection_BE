from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PredictionResponse(BaseModel):
    id: int
    scan_id: int
    prediction: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True


class ScanResponse(BaseModel):
    id: int
    file_path: str
    uploaded_at: datetime
    prediction: Optional[PredictionResponse] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
