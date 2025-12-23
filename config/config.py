from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Enterprise Backend"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    LOG_LEVEL: str = "INFO"

    LLM_API_KEY: str 
    LLM_BASE_URL: str
    LLM_MODEL_NAME: str 
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
