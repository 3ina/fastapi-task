from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db
from app.infrastructure.models import (
    OrderORM,
    PassengerORM,
    TicketORM,
    UserORM,
    AirportORM,
)
from app.infrastructure.airportRepository import AirportRepository
from app.infrastructure.passengerRepository import PassengerRepository
from app.infrastructure.ticketRepository import TicketRepository
from app.infrastructure.userRepository import UserRepository
from app.infrastructure.orderRepository import OrderRepository
from app.services.passengerService import PassengerService
from app.services.userService import UserService
from app.services.orderService import OrderService
from app.selectors.passengersSelector import PassengerSelector
from app.selectors.airportSelector import AirportSelector
from app.selectors.flightSelector import FlightSelector
from app.selectors.userSelector import UserSelector


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    repo = UserRepository(model=UserORM, db=db)
    return repo


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    repo = UserRepository(model=UserORM, db=db)
    service = UserService(user_repo=repo, db=db)
    return service


def get_user_selector(user_repo=Depends(get_user_repo)):
    selector = UserSelector(user_repo=user_repo)
    return selector


def get_passenger_repo(db: AsyncSession = Depends(get_db)) -> PassengerRepository:
    repo = PassengerRepository(model=PassengerORM, db=db)
    return repo


def get_passenger_service(
    db: AsyncSession = Depends(get_db),
) -> PassengerService:
    repo = PassengerRepository(model=PassengerORM, db=db)
    service = PassengerService(passenger_repo=repo, db=db)
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


def get_flight_selector() -> FlightSelector:
    flight_selector = FlightSelector()
    return flight_selector


def get_order_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    order_repo = OrderRepository(model=OrderORM, db=db)
    passenger_repo = PassengerRepository(model=PassengerORM, db=db)
    ticket_repo = TicketRepository(model=TicketORM, db=db)
    flight_selector = FlightSelector()
    airport_repo = AirportRepository(model=AirportORM, db=db)
    service = OrderService(
        db=db,
        order_repo=order_repo,
        passenger_repo=passenger_repo,
        ticket_repo=ticket_repo,
        flight_selector=flight_selector,
        airport_repo=airport_repo,
    )
    return service
