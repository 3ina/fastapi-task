from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Any


class NormalizedFlight(BaseModel):
    id: str
    source: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    price: Decimal = Field(decimal_places=4, max_digits=19)


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
