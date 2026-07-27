"""
Application configuration loaded from environment variables.

Uses pydantic-settings for type-safe config management.
Never hardcode secrets — always use environment variables.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = ""
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Return cached settings instance.
    lru_cache ensures settings are only loaded once.
    """
    return Settings()


settings = get_settings()
