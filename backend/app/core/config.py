# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    # DB
    DATABASE_URL: str

    # Auth / Security
    JWT_SECRET: str = "dev-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # App
    APP_NAME: str = "training-hub"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[AnyHttpUrl] = []

settings = Settings()
