from datetime import UTC, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.external_apis.flightAdaptor import NormalizedFlight
from app.infrastructure.models import AirportORM
from app.infrastructure.passengerRepository import PassengerRepository
from app.infrastructure.ticketRepository import CreateTicketSchema, TicketRepository
from app.infrastructure.orderRepository import OrderRepository
from app.infrastructure.airportRepository import AirportRepository
from app.selectors.flightSelector import FlightSelector
from app.exceptions.flightException import FlightNotFound
from app.infrastructure.orderRepository import CreateOrderSchema
from app.core.utils import generate_random_code
from app.exceptions.airportException import AirportNotFound


class OrderService:
    def __init__(
        self,
        *,
        db: AsyncSession,
        order_repo: OrderRepository,
        passenger_repo: PassengerRepository,
        ticket_repo: TicketRepository,
        flight_selector: FlightSelector,
        airport_repo: AirportRepository,
    ):
        self.order_repo = order_repo
        self.passenger_repo = passenger_repo
        self.ticket_repo = ticket_repo
        self.flighet_selector = flight_selector
        self.airport_repo = airport_repo
        self.db = db

    async def submit_order(
        self, *, user_id: int, passengers_id: list[int], flight_id: str
    ):
        flights: list[
            NormalizedFlight
        ] = await self.flighet_selector.get_all_normalized_flights()
        selected_flight: NormalizedFlight | None = None
        for flight in flights:
            if flight.id == flight_id:
                selected_flight = flight

        if selected_flight is None:
            raise FlightNotFound("selected flight not found")
        destination_airport: (
            AirportORM | None
        ) = await self.airport_repo.get_airport_by_code(
            code=selected_flight.destination
        )
        if destination_airport is None:
            raise AirportNotFound(
                f"airport with code {selected_flight.destination} not found"
            )

        origin_airport: AirportORM | None = await self.airport_repo.get_airport_by_code(
            code=selected_flight.origin
        )
        if origin_airport is None:
            raise AirportNotFound(
                f"airport with code {selected_flight.origin} not found"
            )

        create_schema = CreateOrderSchema(
            user_id=user_id,
            flight_id=flight_id,
            destination_id=destination_airport.id,
            origin_id=origin_airport.id,
            departure_time=datetime.fromisoformat(selected_flight.departure_time),
            arrival_time=datetime.fromisoformat(selected_flight.arrival_time),
            code=generate_random_code(length=10)
            + str(user_id)
            + datetime.now(UTC).isoformat(),
        )

        order = await self.order_repo.create(obj_in=create_schema)

        for passenger_id in passengers_id:
            if (
                await self.passenger_repo.get_passenger_for_user(
                    user_id=user_id, passenger_id=passenger_id
                )
                is not None
            ):
                obi_in_ticket = CreateTicketSchema(
                    ticket_number=generate_random_code()
                    + str(passenger_id)
                    + str(user_id)
                    + datetime.now(UTC).isoformat(),
                    order_id=order.id,
                    passenger_id=passenger_id,
                    price=selected_flight.price,
                )

                await self.ticket_repo.create(obj_in=obi_in_ticket)
        await self.db.commit()
        return {
            "message": "order submited successfully",
            "data": {"order_id": order.id},
        }
