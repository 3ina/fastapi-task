from pydantic import BaseModel
from typing import Any
import asyncio
from app.external_apis.mock_api import (
    mock_fetch_flights_from_a,
    mock_fetch_flights_from_b,
)


class NormalizedFlight(BaseModel):
    id: str
    source: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    price: float


class FlightAdaptor:
    def __init__(self, source_name: str, mapping: dict[str, str]):
        self.source_name = source_name
        self.mapping = mapping

    def adapt(self, raw_flight: dict[str, Any]) -> NormalizedFlight:
        normalized_data = {
            standard_key: raw_flight[source_key]
            for standard_key, source_key in self.mapping.items()
        }
        normalized_data["source"] = self.source_name

        return NormalizedFlight(**normalized_data)


async def get_all_normalized_flights() -> list[NormalizedFlight]:
    flights_a_raw, flights_b_raw = await asyncio.gather(
        mock_fetch_flights_from_a(), mock_fetch_flights_from_b()
    )

    MAPPING_A = {
        "id": "id",
        "origin": "from",
        "destination": "to",
        "departure_time": "departure",
        "arrival_time": "arrival",
        "price": "price",
    }
    MAPPING_B = {
        "id": "flight_id",
        "origin": "origin",
        "destination": "destination",
        "departure_time": "departure_time",
        "arrival_time": "arrival_time",
        "price": "price",
    }

    adaptor_a = FlightAdaptor(source_name="Source A", mapping=MAPPING_A)
    adaptor_b = FlightAdaptor(source_name="Source B", mapping=MAPPING_B)

    normalized_a = [adaptor_a.adapt(flight) for flight in flights_a_raw]
    normalized_b = [adaptor_b.adapt(flight) for flight in flights_b_raw]

    all_flights = normalized_a + normalized_b

    return all_flights
