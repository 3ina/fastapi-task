from typing import Optional
from pydantic import BaseModel
from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import OrderORM


class CreateOrderSchema(BaseModel):
    code: str
    price: float
    user_id: int


class UpdateOrderSchema(BaseModel):
    code: Optional[str] = None
    price: Optional[float] = None
    user_id: Optional[int] = None


class OrderRepository(BaseRepository[OrderORM, CreateOrderSchema, UpdateOrderSchema]):
    def update(self, *args, **kwargs):
        raise NotImplementedError("orders are immutable")
