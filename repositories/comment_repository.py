from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(self, task_id: int, author_id: int, content: str) -> Comment:
        comment = Comment(task_id=task_id, author_id=author_id, content=content)
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def get_task_comments(self, task_id: int) -> list[Comment]:
        result = await self.db.execute(
            select(Comment).filter(Comment.task_id == task_id).order_by(Comment.id.asc())
        )
        return result.scalars().all()
