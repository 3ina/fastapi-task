from typing import Optional
from datetime import datetime
from pydantic import BaseModel


from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import OrderORM


class CreateOrderSchema(BaseModel):
    code: str
    user_id: int
    destination_id: int
    origin_id: int
    flight_id: str
    departure_time: datetime
    arrival_time: datetime


class UpdateOrderSchema(BaseModel):
    code: str | None = None
    user_id: int | None = None
    destination_id: int | None = None
    origin_id: int | None = None
    flight_id: str | None = None
    departure_time: datetime | None = None
    arrival_time: datetime | None = None


class OrderRepository(BaseRepository[OrderORM, CreateOrderSchema, UpdateOrderSchema]):
    def update(self, *args, **kwargs):
        raise NotImplementedError("orders are immutable")
