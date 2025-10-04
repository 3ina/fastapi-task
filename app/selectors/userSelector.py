from app.infrastructure.userRepository import UserRepository
from app.infrastructure.models import UserORM
from app.exceptions.userService import UsernameNotFound


class UserSelector:
    def __init__(self, *, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_by_username(self, *, username: str) -> UserORM | None:
        db_user = await self.user_repo.get_by_username(username)
        if db_user is None:
            raise UsernameNotFound(f"username : {username} not found ")

        return db_user
