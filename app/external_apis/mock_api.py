import asyncio
from typing import Any


async def mock_fetch_flights_from_a() -> list[dict[str, Any]]:
    await asyncio.sleep(0.2)
    return [
        {
            "id": "A123",
            "from": "THR",
            "to": "MHD",
            "departure": "2025-11-04T10:00:00",
            "arrival": "2025-11-04T11:30:00",
            "price": 150.50,
        },
        {
            "id": "A124",
            "from": "THR",
            "to": "SYD",
            "departure": "2025-11-04T15:30:00",
            "arrival": "2025-11-04T03:00:00",
            "price": 890.99,
        },
        {
            "id": "A125",
            "from": "MHD",
            "to": "DXB",
            "departure": "2025-11-04T18:00:00",
            "arrival": "2025-11-04T21:45:00",
            "price": 210.00,
        },
        {
            "id": "A126",
            "from": "THR",
            "to": "ISF",
            "departure": "2025-11-04T08:15:00",
            "arrival": "2025-11-04T09:40:00",
            "price": 110.00,
        },
        {
            "id": "A127",
            "from": "MHD",
            "to": "THR",
            "departure": "2025-11-04T11:45:00",
            "arrival": "2025-11-04T13:10:00",
            "price": 165.75,
        },
        {
            "id": "A128",
            "from": "DXB",
            "to": "THR",
            "departure": "2025-11-04T22:00:00",
            "arrival": "2025-11-04T00:30:00",
            "price": 250.00,
        },
        {
            "id": "A129",
            "from": "ISF",
            "to": "MHD",
            "departure": "2025-11-04T07:30:00",
            "arrival": "2025-11-04T08:55:00",
            "price": 180.00,
        },
    ]


async def mock_fetch_flights_from_b() -> list[dict[str, Any]]:
    await asyncio.sleep(0.2)
    return [
        {
            "flight_id": "B456",
            "origin": "THR",
            "destination": "ISF",
            "departure_time": "2025-11-04T11:30:00",
            "arrival_time": "2025-11-04T13:00:00",
            "price": 120.00,
        },
        {
            "flight_id": "B789",
            "origin": "THR",
            "destination": "MHD",
            "departure_time": "2025-11-04T09:00:00",
            "arrival_time": "2025-11-04T10:20:00",
            "price": 145.00,
        },
        {
            "flight_id": "B457",
            "origin": "THR",
            "destination": "DXB",
            "departure_time": "2025-11-04T16:00:00",
            "arrival_time": "2025-11-04T19:50:00",
            "price": 205.50,
        },
        {
            "flight_id": "B458",
            "origin": "ISF",
            "destination": "THR",
            "departure_time": "2025-11-04T20:45:00",
            "arrival_time": "2025-11-04T22:15:00",
            "price": 130.00,
        },
        {
            "flight_id": "B459",
            "origin": "MHD",
            "destination": "THR",
            "departure_time": "2025-11-04T12:00:00",
            "arrival_time": "2025-11-04T13:35:00",
            "price": 155.00,
        },
        {
            "flight_id": "B460",
            "origin": "SYD",
            "destination": "DXB",
            "departure_time": "2025-11-04T23:00:00",
            "arrival_time": "2025-11-04T05:30:00",
            "price": 750.00,
        },
        {
            "flight_id": "B461",
            "origin": "THR",
            "destination": "MHD",
            "departure_time": "2025-11-04T14:30:00",
            "arrival_time": "2025-11-04T16:05:00",
            "price": 148.00,
        },
        {
            "flight_id": "B462",
            "origin": "ISF",
            "destination": "THR",
            "departure_time": "2025-11-04T19:00:00",
            "arrival_time": "2025-11-04T20:25:00",
            "price": 125.00,
        },
    ]
