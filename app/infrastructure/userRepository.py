from typing import Optional
from pydantic import BaseModel
from sqlalchemy import select
from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import UserORM


class CreateUserSchema(BaseModel):
    username: str
    password: str
    name: str
    phone_number: str


class UpdateUserSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    name: str | None = None
    phone_number: str | None = None


class UserRepository(BaseRepository[UserORM, CreateUserSchema, UpdateUserSchema]):
    async def get_by_username(self, username: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.username == username)
        db_result = await self.db.execute(stmt)
        return db_result.scalar_one_or_none()
