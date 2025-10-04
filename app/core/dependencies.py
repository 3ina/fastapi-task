from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.infrastructure.models import PassengerORM, UserORM, AirportORM
from app.infrastructure.airportRepository import AirportRepository
from app.infrastructure.passengerRepository import PassengerRepository
from app.infrastructure.userRepository import UserRepository
from app.services.passengerService import PassengerService
from app.services.userService import UserService
from app.selectors.passengersSelector import PassengerSelector
from app.selectors.airportSelector import AirportSelector


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    repo = UserRepository(model=UserORM, db=db)
    return repo


def get_user_service(user_repo: UserRepository = Depends(get_user_repo)) -> UserService:
    service = UserService(user_repo=user_repo)
    return service


def get_passenger_repo(db: AsyncSession = Depends(get_db)) -> PassengerRepository:
    repo = PassengerRepository(model=PassengerORM, db=db)
    return repo


def get_passenger_service(
    passenger_repo: PassengerRepository = Depends(get_passenger_repo),
) -> PassengerService:
    service = PassengerService(passenger_repo=passenger_repo)
    return service


def get_passenger_selector(
    passenger_repo: PassengerRepository = Depends(get_passenger_repo),
) -> PassengerSelector:
    selector = PassengerSelector(passenger_repo=passenger_repo)
    return selector


def get_airport_repo(db: AsyncSession = Depends(get_db)) -> AirportRepository:
    repo = AirportRepository(model=AirportORM, db=db)
    return repo


def get_airport_selector(
    airport_repo: AirportRepository = Depends(get_airport_repo),
) -> AirportSelector:
    selector = AirportSelector(airport_repo=airport_repo)
    return selector
