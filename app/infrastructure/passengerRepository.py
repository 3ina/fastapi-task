from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import Gender, PassengerORM


class CreatePassengerSchema(BaseModel):
    name: str
    national_id: str
    date_of_birth: date
    gender: Gender


class UpdatePassengerSchema(BaseModel):
    name: str | None = None
    national_id: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None


class PassengerRepository(
    BaseRepository[PassengerORM, CreatePassengerSchema, UpdatePassengerSchema]
):
    pass
