import pytest
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from app.infrastructure.models import (
    TicketORM,
    OrderORM,
    PassengerORM,
    UserORM,
    AirportORM,
)
from app.infrastructure.ticketRepository import TicketRepository, CreateTicketSchema
from app.infrastructure.orderRepository import OrderRepository, CreateOrderSchema
from app.infrastructure.passengerRepository import (
    PassengerRepository,
    CreatePassengerSchema,
)
from app.infrastructure.userRepository import UserRepository, CreateUserSchema
from app.infrastructure.airportRepository import AirportRepository, CreateAirportSchema


@pytest.mark.asyncio
class TestTicketRepository:
    async def test_ticket_insert_fails_when_parent_missing(self, async_session):
        """FK error when either order or passenger does not exist."""
        repo = TicketRepository(model=TicketORM, db=async_session)

        ticket = CreateTicketSchema(
            ticket_number="TK-999",
            order_id=999,
            passenger_id=999,
            price=Decimal("120.50"),
        )

        await repo.create(obj_in=ticket)

        with pytest.raises(IntegrityError):
            await async_session.commit()

    async def test_ticket_insert_succeeds_when_parents_exist(
        self,
        async_session,
        sample_user_data,
        sample_passenger_data,
    ):
        """Insert succeeds after creating required parents (user→order, passenger)."""
        user_repo = UserRepository(model=UserORM, db=async_session)
        airport_repo = AirportRepository(model=AirportORM, db=async_session)
        order_repo = OrderRepository(model=OrderORM, db=async_session)
        passenger_repo = PassengerRepository(model=PassengerORM, db=async_session)

        user = await user_repo.create(obj_in=CreateUserSchema(**sample_user_data))
        dest = await airport_repo.create(
            obj_in=CreateAirportSchema(name="Dest", code="DST")
        )
        orig = await airport_repo.create(
            obj_in=CreateAirportSchema(name="Orig", code="ORG")
        )
        from datetime import datetime

        await async_session.flush()
        order = await order_repo.create(
            obj_in=CreateOrderSchema(
                code="ORD-TK",
                user_id=user.id,
                destination_id=dest.id,
                origin_id=orig.id,
                flight_id="FL-TK",
                departure_time=datetime(2023, 1, 1, 10, 0),
                arrival_time=datetime(2023, 1, 1, 12, 0),
            )
        )
        passenger_data = sample_passenger_data.copy()
        passenger_data["user_id"] = user.id
        passenger = await passenger_repo.create(
            obj_in=CreatePassengerSchema(**passenger_data)
        )

        await async_session.flush()

        ticket_repo = TicketRepository(model=TicketORM, db=async_session)
        ticket_schema = CreateTicketSchema(
            ticket_number="TK-OK",
            order_id=order.id,
            passenger_id=passenger.id,
            price=Decimal("99.99"),
        )
        db_ticket = await ticket_repo.create(obj_in=ticket_schema)
        await async_session.commit()

        assert db_ticket.id is not None
        assert db_ticket.order_id == order.id
        assert db_ticket.passenger_id == passenger.id
        assert db_ticket.price == Decimal("99.99")
