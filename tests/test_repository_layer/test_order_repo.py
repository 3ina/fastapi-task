import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.infrastructure.models import OrderORM, UserORM, AirportORM
from app.infrastructure.orderRepository import OrderRepository, CreateOrderSchema
from app.infrastructure.userRepository import UserRepository, CreateUserSchema
from app.infrastructure.airportRepository import AirportRepository, CreateAirportSchema


@pytest.mark.asyncio
class TestOrderRepository:
    async def test_order_insert_fails_when_user_or_airport_missing(self, async_session):
        repo = OrderRepository(model=OrderORM, db=async_session)

        order = CreateOrderSchema(
            code="ORD-123",
            user_id=999,
            destination_id=999,
            origin_id=888,
            flight_id="FL-123",
            departure_time=datetime(2023, 1, 1, 10, 0),
            arrival_time=datetime(2023, 1, 1, 12, 0),
        )

        await repo.create(obj_in=order)

        with pytest.raises(IntegrityError):
            await async_session.commit()

    async def test_order_insert_succeeds_when_parents_exist(
        self,
        async_session,
        sample_user_data,
    ):
        """Insert succeeds after creating required parents."""
        user_repo = UserRepository(model=UserORM, db=async_session)
        airport_repo = AirportRepository(model=AirportORM, db=async_session)

        user = await user_repo.create(obj_in=CreateUserSchema(**sample_user_data))
        dest = await airport_repo.create(
            obj_in=CreateAirportSchema(name="Dest", code="DST")
        )
        orig = await airport_repo.create(
            obj_in=CreateAirportSchema(name="Orig", code="ORG")
        )
        await async_session.flush()
        order_repo = OrderRepository(model=OrderORM, db=async_session)
        order = CreateOrderSchema(
            code="ORD-OK",
            user_id=user.id,
            destination_id=dest.id,
            origin_id=orig.id,
            flight_id="FL-OK",
            departure_time=datetime(2023, 1, 1, 10, 0),
            arrival_time=datetime(2023, 1, 1, 12, 0),
        )

        db_order = await order_repo.create(obj_in=order)
        await async_session.commit()

        assert db_order.id is not None
        assert db_order.user_id == user.id
        assert db_order.destination_id == dest.id
        assert db_order.origin_id == orig.id
