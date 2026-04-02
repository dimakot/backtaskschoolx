from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from minio import Minio
from minio.error import S3Error

from auth.dependencies import get_current_user
from core.config import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
from core.exceptions import TaskNotFound
from database.db import get_db
from database.models import User
from repositories.task_repository import TaskRepository

router = APIRouter(prefix="/v1/tasks", tags=["Files"])

minio_client = Minio(
    MINIO_URL.replace("http://", "").replace("https://", ""),
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)


@router.post("/{task_id}/upload-avatar")
async def upload_avatar(
    task_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = await task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if task is None:
        raise TaskNotFound()

    try:
        if not minio_client.bucket_exists(MINIO_BUCKET):
            minio_client.make_bucket(MINIO_BUCKET)
    except S3Error:
        pass

    file_name = f"tasks/{task_id}/{file.filename}"
    content = await file.read()

    try:
        minio_client.put_object(
            MINIO_BUCKET,
            file_name,
            content,
            len(content),
            content_type=file.content_type,
        )
    except S3Error as e:
        raise e

    url = f"{MINIO_URL}/{MINIO_BUCKET}/{file_name}"
    return {"url": url}
