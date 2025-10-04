from datetime import date
from typing import List, Literal, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import PassengerORM


class CreatePassengerSchema(BaseModel):
    user_id: int
    name: str
    national_id: str
    date_of_birth: date
    gender: Literal["men", "women"]


class UpdatePassengerSchema(BaseModel):
    name: str | None = None
    national_id: str | None = None
    date_of_birth: date | None = None
    gender: Literal["men", "women"] | None = None


class PassengerRepository(
    BaseRepository[PassengerORM, CreatePassengerSchema, UpdatePassengerSchema]
):
    async def get_passengers_for_user(self, *, user_id: int) -> Sequence[PassengerORM]:
        stmt = select(PassengerORM).where(PassengerORM.user_id == user_id)
        passengers = await self.db.execute(stmt)
        passengers = passengers.scalars().all()
        return passengers

    async def get_passenger_for_user(
        self, *, user_id: int, passenger_id: int
    ) -> PassengerORM | None:
        stmt = select(PassengerORM).where(
            PassengerORM.id == passenger_id, PassengerORM.user_id == user_id
        )
        passenger = await self.db.execute(stmt)
        passenger = passenger.scalar_one_or_none()
        return passenger
