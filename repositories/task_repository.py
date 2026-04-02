from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Task
from schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task_data: TaskCreate, owner_id: int) -> Task:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            owner_id=owner_id,
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_all_tasks(self, owner_id: int) -> list[Task]:
        result = await self.db.execute(
            select(Task).filter(Task.owner_id == owner_id)
        )
        return result.scalars().all()

    async def get_task_by_id(self, task_id: int, owner_id: int) -> Task | None:
        result = await self.db.execute(
            select(Task).filter(Task.id == task_id, Task.owner_id == owner_id)
        )
        return result.scalars().first()

    async def update_task(self, task: Task, task_data: TaskUpdate) -> Task:
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.status is not None:
            task.status = task_data.status
        if task_data.priority is not None:
            task.priority = task_data.priority

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()
