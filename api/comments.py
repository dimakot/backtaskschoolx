from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from core.exceptions import CommentNotFound, TaskNotFound
from database.db import get_db
from database.models import User
from repositories.comment_repository import CommentRepository
from repositories.task_repository import TaskRepository
from schemas.comment import CommentCreate, CommentResponse


router = APIRouter(prefix="/v1/tasks", tags=["Comments"])


@router.post("/{task_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    task_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = await task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if task is None:
        raise TaskNotFound()

    comment_repo = CommentRepository(db)
    return await comment_repo.create_comment(
        task_id=task_id,
        author_id=current_user.id,
        content=data.content,
    )


@router.get("/{task_id}/comments", response_model=list[CommentResponse])
async def get_comments(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = await task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if task is None:
        raise TaskNotFound()

    comment_repo = CommentRepository(db)
    comments = await comment_repo.get_task_comments(task_id=task_id)
    if not comments:
        raise CommentNotFound("Комментарии не найдены")
    return comments
