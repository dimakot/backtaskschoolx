from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from core.exceptions import CommentNotFound, TaskNotFound
from database.db import get_db
from database.models import User
from repositories.comment_repository import CommentRepository
from repositories.task_repository import TaskRepository
from schemas.comment import CommentCreate, CommentResponse


router = APIRouter(prefix="/v1/tasks", tags=["Comments"])


@router.post("/{task_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    task_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if task is None:
        raise TaskNotFound()

    comment_repo = CommentRepository(db)
    return comment_repo.create_comment(
        task_id=task_id,
        author_id=current_user.id,
        content=data.content,
    )


@router.get("/{task_id}/comments", response_model=list[CommentResponse])
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if task is None:
        raise TaskNotFound()

    comment_repo = CommentRepository(db)
    comments = comment_repo.get_task_comments(task_id=task_id)
    if not comments:
        raise CommentNotFound("Комментарии не найдены")
    return comments
