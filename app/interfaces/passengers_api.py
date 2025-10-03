from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.core.dependencies import get_passenger_service
from app.infrastructure.models import UserORM
from app.services.passengerService import PassengerService

router = APIRouter(prefix="/passengers", tags=["Passengers"])


class CreatePassengerRequest(BaseModel):
    national_id: str
    name: str
    date_of_birth: date
    gender: Literal["men", "women"]


class PassengerData(BaseModel):
    national_id: str
    name: str


class CreatePassengerResponse(BaseModel):
    message: str
    data: PassengerData


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CreatePassengerResponse,
)
async def create_passenger(
    data: CreatePassengerRequest,
    passengers_service: PassengerService = Depends(get_passenger_service),
    current_user: UserORM = Depends(get_current_user),
):
    return await passengers_service.create_passenger(
        user_id=current_user.id,
        national_id=data.national_id,
        name=data.name,
        gender=data.gender,
        date_of_birth=data.date_of_birth,
    )
