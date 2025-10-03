from app.infrastructure.passengerRepository import (
    PassengerRepository,
)
from app.core.utils import calculate_age


class PassengerSelector:
    def __init__(self, *, passenger_repo: PassengerRepository):
        self.passenger_repo = passenger_repo

    async def get_passengers_for_user(self, *, user_id: int):
        res = []
        db_passengers = await self.passenger_repo.get_passengers_for_user(
            user_id=user_id
        )
        for passenger in db_passengers:
            res.append(
                {
                    "id": passenger.id,
                    "national_id": passenger.national_id,
                    "name": passenger.name,
                    "age": calculate_age(passenger.date_of_birth),
                    "gender": passenger.gender,
                }
            )
        return res
