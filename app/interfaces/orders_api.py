from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.dependencies import get_order_service
from app.infrastructure.models import UserORM
from app.services.orderService import OrderService


router = APIRouter(prefix="/orders", tags=["Orders"])


class CreateOrderRequest(BaseModel):
    passengers_id: list[int]
    flight_id: str


@router.post("/", status_code=status.HTTP_200_OK)
async def create_order(
    data: CreateOrderRequest,
    order_service: OrderService = Depends(get_order_service),
    current_user: UserORM = Depends(get_current_user),
):
    return await order_service.submit_order(
        user_id=current_user.id,
        passengers_id=data.passengers_id,
        flight_id=data.flight_id,
    )
