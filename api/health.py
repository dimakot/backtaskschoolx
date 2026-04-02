from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from minio import Minio
from minio.error import S3Error

from core.config import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET, APP_VERSION, APP_ENV
from database.db import get_db

router = APIRouter(tags=["Health"])

minio_client = Minio(
    MINIO_URL.replace("http://", "").replace("https://", ""),
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)


@router.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    db_status = "down"
    minio_status = "down"

    try:
        await db.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        pass

    try:
        minio_client.list_buckets()
        minio_status = "up"
    except S3Error:
        pass

    return {
        "status": "ok" if db_status == "up" and minio_status == "up" else "degraded",
        "database": db_status,
        "minio": minio_status,
    }


@router.get("/info")
async def info():
    return {
        "version": APP_VERSION,
        "environment": APP_ENV,
    }
