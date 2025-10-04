from pydantic import BaseModel
from sqlalchemy import select

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
    async def get_airport_by_code(self, *, code: str) -> AirportORM | None:
        stmt = select(AirportORM).where(AirportORM.code == code)
        db_airport = await self.db.execute(stmt)
        db_airport = db_airport.scalar_one_or_none()
        return db_airport
