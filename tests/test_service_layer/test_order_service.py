import pytest
from datetime import datetime, UTC, date
from decimal import Decimal
from unittest.mock import AsyncMock

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.infrastructure.models import (
    UserORM,
    AirportORM,
    PassengerORM,
    OrderORM,
    TicketORM,
)
from app.infrastructure.orderRepository import OrderRepository
from app.infrastructure.passengerRepository import (
    CreatePassengerSchema,
    PassengerRepository,
)
from app.infrastructure.ticketRepository import TicketRepository
from app.infrastructure.airportRepository import AirportRepository, CreateAirportSchema
from app.infrastructure.userRepository import CreateUserSchema, UserRepository
from app.selectors.flightSelector import FlightSelector
from app.services.orderService import OrderService
from app.external_apis.flightAdaptor import NormalizedFlight
from app.exceptions.flightException import FlightNotFound
from app.exceptions.airportException import AirportNotFound


pytestmark = pytest.mark.asyncio


class TestOrderService:
    async def _add_test_airports(self, airport_repo: AirportRepository):
        schema_in = CreateAirportSchema(
            name="Origin",
            code="ORG",
        )
        await airport_repo.create(obj_in=schema_in)
        schema_in = CreateAirportSchema(
            name="Destination",
            code="DST",
        )

        await airport_repo.create(obj_in=schema_in)

    async def _add_test_user(self, user_repo: UserRepository) -> UserORM:
        schema_in = CreateUserSchema(
            username="u1",
            password="p",
            name="n",
            phone_number="123",
        )

        return await user_repo.create(obj_in=schema_in)

    async def _add_test_passenger(
        self, passenger_repo: PassengerRepository, user: UserORM
    ) -> PassengerORM:
        schema_in = CreatePassengerSchema(
            user_id=user.id,
            name="John",
            national_id="N123",
            date_of_birth=date(1990, 1, 1),
            gender="men",
        )

        return await passenger_repo.create(obj_in=schema_in)

    async def test_submit_order_happy_path(self, async_session):
        user_repo = UserRepository(model=UserORM, db=async_session)
        airport_repo = AirportRepository(model=AirportORM, db=async_session)
        order_repo = OrderRepository(model=OrderORM, db=async_session)
        passenger_repo = PassengerRepository(model=PassengerORM, db=async_session)
        ticket_repo = TicketRepository(model=TicketORM, db=async_session)

        flight_selector = FlightSelector()
        flight_selector.get_all_normalized_flights = AsyncMock(
            return_value=[
                NormalizedFlight(
                    id="FL-123",
                    source="A API",
                    origin="ORG",
                    destination="DST",
                    departure_time="2023-01-01T10:00:00+00:00",
                    arrival_time="2023-01-01T12:00:00+00:00",
                    price=Decimal("120.50"),
                )
            ]
        )

        user = await self._add_test_user(user_repo)
        await async_session.flush()
        await self._add_test_airports(airport_repo)
        passenger = await self._add_test_passenger(passenger_repo, user)
        await async_session.flush()

        svc = OrderService(
            db=async_session,
            order_repo=order_repo,
            passenger_repo=passenger_repo,
            ticket_repo=ticket_repo,
            flight_selector=flight_selector,
            airport_repo=airport_repo,
        )

        resp = await svc.submit_order(
            user_id=user.id,
            passengers_id=[passenger.id],
            flight_id="FL-123",
        )

        assert resp["message"] == "order submited successfully"
        order_id = resp["data"]["order_id"]

        order = await order_repo.get(order_id)
        assert order is not None
        assert order.user_id == user.id
        assert order.flight_id == "FL-123"

        tickets = await async_session.scalars(
            select(TicketORM).where(TicketORM.order_id == order_id)
        )
        ticket = tickets.one()
        assert ticket.passenger_id == passenger.id
        assert ticket.price == Decimal("120.50")

    async def test_submit_order_flight_not_found(self, async_session):
        """Raises FlightNotFound when flight_id does not exist."""
        flight_selector = FlightSelector()
        flight_selector.get_all_normalized_flights = AsyncMock(return_value=[])

        svc = OrderService(
            db=async_session,
            order_repo=OrderRepository(model=OrderORM, db=async_session),
            passenger_repo=PassengerRepository(model=PassengerORM, db=async_session),
            ticket_repo=TicketRepository(model=TicketORM, db=async_session),
            flight_selector=flight_selector,
            airport_repo=AirportRepository(model=AirportORM, db=async_session),
        )

        with pytest.raises(FlightNotFound):
            await svc.submit_order(
                user_id=1, passengers_id=[], flight_id="NO-SUCH-FLIGHT"
            )

    async def test_submit_order_airport_not_found(self, async_session):
        """Raises AirportNotFound when airports missing in DB."""
        flight_selector = FlightSelector()
        flight_selector.get_all_normalized_flights = AsyncMock(
            return_value=[
                NormalizedFlight(
                    id="FL-XXX",
                    source="A API",
                    origin="XXX",
                    destination="YYY",
                    departure_time="2023-01-01T10:00:00+00:00",
                    arrival_time="2023-01-01T12:00:00+00:00",
                    price=Decimal("100"),
                )
            ]
        )

        svc = OrderService(
            db=async_session,
            order_repo=OrderRepository(model=OrderORM, db=async_session),
            passenger_repo=PassengerRepository(model=PassengerORM, db=async_session),
            ticket_repo=TicketRepository(model=TicketORM, db=async_session),
            flight_selector=flight_selector,
            airport_repo=AirportRepository(model=AirportORM, db=async_session),
        )

        with pytest.raises(AirportNotFound):
            await svc.submit_order(user_id=1, passengers_id=[], flight_id="FL-XXX")
