# tests/test_user_repository.py
import pytest
from app.infrastructure.userRepository import (
    UserRepository,
    CreateUserSchema,
    UpdateUserSchema,
)
from app.infrastructure.models import UserORM


@pytest.mark.asyncio
class TestUserRepository:
    async def test_create_user(self, async_session, sample_user_data):
        repo = UserRepository(model=UserORM, db=async_session)
        user_schema = CreateUserSchema(**sample_user_data)

        user = await repo.create(obj_in=user_schema)
        await async_session.commit()

        assert user.username == sample_user_data["username"]
        assert user.name == sample_user_data["name"]
        assert user.id is not None

    async def test_get_by_username(self, async_session, sample_user_data):
        repo = UserRepository(model=UserORM, db=async_session)
        user_schema = CreateUserSchema(**sample_user_data)
        await repo.create(obj_in=user_schema)
        await async_session.commit()

        retrieved = await repo.get_by_username(username=sample_user_data["username"])
        assert retrieved is not None
        assert retrieved.name == sample_user_data["name"]

    async def test_update_user(self, async_session, sample_user_data):
        repo = UserRepository(model=UserORM, db=async_session)
        user_schema = CreateUserSchema(**sample_user_data)
        user = await repo.create(obj_in=user_schema)
        await async_session.commit()

        update_schema = UpdateUserSchema(name="Updated Name")
        updated = await repo.update(db_obj=user, obj_in=update_schema)
        await async_session.commit()

        assert updated.name == "Updated Name"
        assert updated.username == sample_user_data["username"]
