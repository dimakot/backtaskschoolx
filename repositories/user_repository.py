from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).filter(User.id == user_id)
        )
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).filter(User.username == username)
        )
        return result.scalars().first()

    async def create_user(self, username: str, hashed_password: str) -> User:
        user = User(username=username, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
