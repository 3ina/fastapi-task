from typing import Literal
from app.infrastructure.passengerRepository import (
    PassengerRepository,
    CreatePassengerSchema,
)
from datetime import date


class PassengerService:
    def __init__(self, *, passenger_repo: PassengerRepository):
        self.passenger_repo = passenger_repo

    async def create_passenger(
        self,
        *,
        user_id: int,
        name: str,
        national_id: str,
        gender: Literal["men", "women"],
        date_of_birth: date,
    ):
        # TODO : complete validation and raise ecception in business logic layer
        schema = CreatePassengerSchema(
            user_id=user_id,
            name=name,
            national_id=national_id,
            gender=gender,
            date_of_birth=date_of_birth,
        )
        db_passenger = await self.passenger_repo.create(obj_in=schema)
        return {
            "message": "successfully ad passenger",
            "data": {
                "national_id": db_passenger.national_id,
                "name": db_passenger.name,
            },
        }
