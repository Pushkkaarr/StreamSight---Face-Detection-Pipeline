from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/streamsight"
    ALLOWED_ORIGINS: List[str] = ["*"]
    MAX_QUEUE_SIZE: int = 30
    JPEG_QUALITY: int = 85
    MIN_DETECTION_CONFIDENCE: float = 0.5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
