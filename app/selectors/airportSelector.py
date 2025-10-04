from app.infrastructure.airportRepository import AirportRepository


class AirportSelector:
    def __init__(self, *, airport_repo: AirportRepository):
        self.airport_repo = airport_repo

    async def get_airports(self, *, page: int = 1, size: int = 10):
        res = []
        (db_airports, total_count) = await self.airport_repo.get_multi(
            page=page, size=size
        )
        for db_airport in db_airports:
            res.append(
                {
                    "id": db_airport.id,
                    "name": db_airport.name,
                    "code": db_airport.code,
                }
            )
        return {"airports": res, "total": total_count, "page": page, "size": size}
