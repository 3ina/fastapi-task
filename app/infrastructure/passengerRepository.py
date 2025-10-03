from datetime import date
from typing import Literal

from pydantic import BaseModel

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
    pass
