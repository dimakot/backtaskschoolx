import os

MINIO_URL = os.getenv("MINIO_URL", "http://127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "backtask")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://django:django@localhost:5432/backtask"
)

APP_VERSION = "0.1.0"
APP_ENV = os.getenv("APP_ENV", "development")
