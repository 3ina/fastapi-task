# tests/conftest.py
import pytest
import sys
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Integer
from app.core.database import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
sys.modules["sqlalchemy"].BigInteger = Integer


@pytest.fixture(scope="function")
async def async_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.exec_driver_sql("PRAGMA foreign_keys = ON")
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def sample_airport_data():
    return {"name": "JFK", "code": "JFK"}


@pytest.fixture
def sample_user_data():
    return {
        "username": "testuser",
        "password": "hashedpassword",
        "name": "Test User",
        "phone_number": "1234567890",
    }


@pytest.fixture
def sample_passenger_data():
    return {
        "user_id": 1,
        "name": "John Doe",
        "national_id": "AB123456",
        "date_of_birth": "1990-01-01",
        "gender": "men",
    }
