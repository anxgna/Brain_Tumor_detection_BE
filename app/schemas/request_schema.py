from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class RecordScan(BaseModel):
    user_id: Optional[int] = None
    # the actual file is handled by UploadFile explicitly.
