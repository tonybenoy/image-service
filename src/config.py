import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path("./src") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Settings for the app."""

    POSTGRES_USER: str = str(os.getenv("POSTGRES_USER"))
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "step")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "http://127.0.0.1:9000")
    S3_ACCESS_KEY_ID: str = str(os.getenv("S3_ACCESS_KEY_ID"))
    S3_ACCESS_KEY: str = str(os.getenv("S3_ACCESS_KEY"))
    S3_BUCKET: str = os.getenv("S3_BUCKET", "test")
    RQ_QUEUE_NAME: str = os.getenv("RQ_QUEUE", "default")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
