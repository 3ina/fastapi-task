from typing import Optional

from pydantic import BaseModel

from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import AirportORM


class CreateAirportSchema(BaseModel):
    name: str
    code: str


class UpdateAirportSchema(BaseModel):
    name: str | None = None
    code: str | None = None


class AirportRepository(
    BaseRepository[AirportORM, CreateAirportSchema, UpdateAirportSchema]
):
    pass
