from app.core.utils import get_password_hash, verify_password
from app.exceptions.userService import UsernameNotFound
from app.infrastructure.models import UserORM
from app.infrastructure.userRepository import CreateUserSchema, UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(
        self, *, username: str, password: str, name: str, phone_number: str
    ) -> dict:
        """ """
        hashed_password = get_password_hash(password)

        user_data = CreateUserSchema(
            username=username,
            password=hashed_password,
            name=name,
            phone_number=phone_number,
        )

        db_obj = await self.user_repo.create(obj_in=user_data)
        return {
            "message": "user register successfully",
            "data": {
                "id": db_obj.id,
                "username": db_obj.username,
            },
        }

    async def authenticate_user(
        self, *, username: str, password: str
    ) -> UserORM | None:
        db_user = await self.user_repo.get_by_username(username)
        if db_user is None:
            raise UsernameNotFound(f"username : {username} not found ")

        if verify_password(password, str(db_user.password)):
            return db_user
        return None

    async def get_by_username(self, *, username: str) -> UserORM | None:
        db_user = await self.user_repo.get_by_username(username)
        if db_user is None:
            raise UsernameNotFound(f"username : {username} not found ")

        return db_user
