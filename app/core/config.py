import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_file = ".env"
load_dotenv(env_file)


class Settings(BaseSettings):
    APP_PORT: int = os.getenv("PORT")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    DEBUG: bool = os.getenv("DEBUG")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")


settings = Settings()
