# tests/test_passenger_repository.py
import pytest
from app.infrastructure.passengerRepository import (
    PassengerRepository,
    CreatePassengerSchema,
)
from app.infrastructure.models import PassengerORM, UserORM
from app.infrastructure.userRepository import CreateUserSchema, UserRepository


@pytest.mark.asyncio
class TestPassengerRepository:
    async def test_create_passenger(
        self, async_session, sample_passenger_data, sample_user_data
    ):
        repo = PassengerRepository(model=PassengerORM, db=async_session)
        user_repo = UserRepository(model=UserORM, db=async_session)

        user_schema = CreateUserSchema(**sample_user_data)
        await user_repo.create(obj_in=user_schema)
        passenger_schema = CreatePassengerSchema(**sample_passenger_data)
        await async_session.flush()
        passenger = await repo.create(obj_in=passenger_schema)
        await async_session.commit()

        assert passenger.name == sample_passenger_data["name"]
        assert passenger.national_id == sample_passenger_data["national_id"]
        assert passenger.id is not None

    async def test_get_passengers_for_user(
        self,
        async_session,
        sample_passenger_data,
        sample_user_data,
    ):
        repo = PassengerRepository(model=PassengerORM, db=async_session)
        user_repo = UserRepository(model=UserORM, db=async_session)

        user_schema = CreateUserSchema(**sample_user_data)
        await user_repo.create(obj_in=user_schema)

        await async_session.flush()
        for i in range(2):
            data = sample_passenger_data.copy()
            data["name"] = f"Passenger {i}"
            await repo.create(obj_in=CreatePassengerSchema(**data))
        await async_session.commit()

        passengers = await repo.get_passengers_for_user(user_id=1)
        assert len(passengers) == 2

    async def test_get_passenger_for_user(
        self, async_session, sample_passenger_data, sample_user_data
    ):
        repo = PassengerRepository(model=PassengerORM, db=async_session)
        passenger_schema = CreatePassengerSchema(**sample_passenger_data)
        user_repo = UserRepository(model=UserORM, db=async_session)

        user_schema = CreateUserSchema(**sample_user_data)
        await user_repo.create(obj_in=user_schema)
        await async_session.flush()
        passenger = await repo.create(obj_in=passenger_schema)
        await async_session.commit()

        retrieved = await repo.get_passenger_for_user(
            user_id=sample_passenger_data["user_id"], passenger_id=passenger.id
        )
        assert retrieved is not None
        assert retrieved.name == sample_passenger_data["name"]

        retrieved = await repo.get_passenger_for_user(
            user_id=999, passenger_id=passenger.id
        )
        assert retrieved is None
