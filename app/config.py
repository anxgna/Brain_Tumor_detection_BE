import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Brain Tumor Detection Backend"
    # Using SQLite as a fallback default for ease of local testing unless MySQL is configured
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./brain_tumor.db"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
