from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from core.exceptions import TaskNotFound
from database.models import User
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from database.db import get_db
from repositories.task_repository import TaskRepository
from services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task_service = TaskService(task_repo)
    return task_service.create_task(task, owner_id=current_user.id)


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    return task_repo.get_all_tasks(owner_id=current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if not task:
        raise TaskNotFound()
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if not task:
        raise TaskNotFound()

    return task_repo.update_task(task, task_data)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db)
    task = task_repo.get_task_by_id(task_id=task_id, owner_id=current_user.id)
    if not task:
        raise TaskNotFound()
    task_repo.delete_task(task)
    return {"message": "Задача удалена"}
