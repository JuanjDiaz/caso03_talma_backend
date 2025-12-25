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
    PASWORD_INICIAL: str

    # SMTP Configuration
    # SMTP Configuration (Renamed to avoid .env conflict)
    MAIL_HOST: str = "smtp.mailersend.net"
    MAIL_PORT: int = 2525
    MAIL_USER: str = "MS_8CwHfS@test-zxk54v8nw61ljy6v.mlsender.net"
    MAIL_PASSWORD: str = "mssp.0ZklBbf.3vz9dledrx64kj50.psuBIBS"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
