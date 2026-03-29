from repositories.task_repository import TaskRepository
from schemas.task import TaskCreate


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task_data: TaskCreate, owner_id: int):
        return self.task_repository.create_task(task_data=task_data, owner_id=owner_id)
