from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.core.auth import get_current_user
from app.core.dependencies import get_passenger_service, get_passenger_selector
from app.infrastructure.models import UserORM
from app.services.passengerService import PassengerService
from app.selectors.passengersSelector import PassengerSelector

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


class PassengerDataGetResponse(BaseModel):
    id: int
    national_id: str
    age: int
    gender: str
    name: str


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[PassengerDataGetResponse]
)
async def get_passengers(
    passengers_selector: PassengerSelector = Depends(get_passenger_selector),
    current_user: UserORM = Depends(get_current_user),
):
    return await passengers_selector.get_passengers_for_user(user_id=current_user.id)
