from typing import Optional
from pydantic import BaseModel
from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import UserORM


class CreateUserSchema(BaseModel):
    username: str
    password: str
    name: str
    phone_number: str


class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None


class UserRepository(BaseRepository[UserORM, CreateUserSchema, UpdateUserSchema]):
    pass
