from typing import Optional
from pydantic import BaseModel
from datetime import date
from app.infrastructure.models import PassengerORM, Gender
from app.infrastructure.baseRepository import BaseRepository


class CreatePassengerSchema(BaseModel):
    name: str
    national_id: str
    date_of_birth: date
    gender: Gender


class UpdatePassengerSchema(BaseModel):
    name: Optional[str] = None
    national_id: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None


class PassengerRepository(
    BaseRepository[PassengerORM, CreatePassengerSchema, UpdatePassengerSchema]
):
    pass
