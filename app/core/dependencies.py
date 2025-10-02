from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.infrastructure.models import UserORM
from app.infrastructure.userRepository import UserRepository
from app.services.userService import UserService


def get_user_repo(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(model=UserORM, db=db)
    return repo


def get_user_service(user_repo: UserRepository = Depends(get_user_repo)) -> UserService:
    service = UserService(user_repo=user_repo)
    return service

