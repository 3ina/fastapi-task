from app.infrastructure.userRepository import UserRepository, CreateUserSchema
from app.core.auth import get_password_hash


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
