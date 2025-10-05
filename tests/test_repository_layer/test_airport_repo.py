# tests/test_airport_repository.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.airportRepository import (
    AirportRepository,
    CreateAirportSchema,
    UpdateAirportSchema,
)
from app.infrastructure.models import AirportORM


@pytest.mark.asyncio
class TestAirportRepository:
    async def test_create_airport(
        self, async_session: AsyncSession, sample_airport_data
    ):
        repo = AirportRepository(model=AirportORM, db=async_session)
        airport_schema = CreateAirportSchema(**sample_airport_data)

        airport = await repo.create(obj_in=airport_schema)
        await async_session.commit()
        await async_session.refresh(airport)
        assert airport.name == sample_airport_data["name"]
        assert airport.code == sample_airport_data["code"]
        assert airport.id is not None

    async def test_get_airport_by_id(self, async_session, sample_airport_data):
        repo = AirportRepository(model=AirportORM, db=async_session)
        airport_schema = CreateAirportSchema(**sample_airport_data)
        created = await repo.create(obj_in=airport_schema)
        await async_session.commit()

        retrieved = await repo.get(created.id)
        assert retrieved is not None
        assert retrieved.code == sample_airport_data["code"]
        assert retrieved.name == sample_airport_data["name"]

    async def test_get_airport_by_code(self, async_session, sample_airport_data):
        repo = AirportRepository(model=AirportORM, db=async_session)
        airport_schema = CreateAirportSchema(**sample_airport_data)
        await repo.create(obj_in=airport_schema)
        await async_session.commit()

        retrieved = await repo.get_airport_by_code(code=sample_airport_data["code"])
        assert retrieved is not None
        assert retrieved.name == sample_airport_data["name"]
        assert retrieved.code == sample_airport_data["code"]

    async def test_update_airport(self, async_session, sample_airport_data):
        repo = AirportRepository(model=AirportORM, db=async_session)
        airport_schema = CreateAirportSchema(**sample_airport_data)
        airport = await repo.create(obj_in=airport_schema)
        await async_session.commit()

        update_schema = UpdateAirportSchema(name="Updated Airport")
        updated = await repo.update(db_obj=airport, obj_in=update_schema)
        await async_session.commit()

        assert updated.name == "Updated Airport"
        assert updated.code == sample_airport_data["code"]

    async def test_remove_airport(self, async_session, sample_airport_data):
        repo = AirportRepository(model=AirportORM, db=async_session)
        airport_schema = CreateAirportSchema(**sample_airport_data)
        airport = await repo.create(obj_in=airport_schema)
        await async_session.commit()

        removed = await repo.remove(id=airport.id)
        await async_session.commit()

        assert removed is not None
        assert await repo.get(airport.id) is None

    async def test_get_multi_pagination(self, async_session):
        repo = AirportRepository(model=AirportORM, db=async_session)

        for i in range(15):
            await repo.create(
                obj_in=CreateAirportSchema(name=f"Airport {i}", code=f"A{i}")
            )
        await async_session.commit()

        airports, total = await repo.get_multi(page=1, size=10)
        assert total == 15
        assert len(airports) == 10

        airports, total = await repo.get_multi(page=2, size=10)
        assert total == 15
        assert len(airports) == 5
