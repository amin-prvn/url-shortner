from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    ENV_NAME: str = "Local"
    BASE_URL: str = "http://localhost:8000"
    DB_HOST:str = "localhost"
    DB_NAME: str  = "url-shortner"
    DB_USER: str = "amin"
    DB_PASSWORD: str = "amin123"
    DB_CONFIG: str = ""

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.DB_CONFIG = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
    print(f"Loading settings: {settings.dict()}")
    return settings
