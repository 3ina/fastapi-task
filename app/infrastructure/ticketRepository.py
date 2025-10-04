from decimal import Decimal
from pydantic import BaseModel, Field

from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import TicketORM


class CreateTicketSchema(BaseModel):
    ticket_number: str
    order_id: int
    passenger_id: int
    price: Decimal = Field(decimal_places=4, max_digits=19)


class UpdateTicketSchema(BaseModel):
    ticket_number: str | None = None
    order_id: int | None = None
    passenger_id: int | None = None
    price: Decimal | None = Field(decimal_places=4, max_digits=19)


class TicketRepository(
    BaseRepository[TicketORM, CreateTicketSchema, UpdateTicketSchema]
):
    def update(self, *args, **kwargs):
        raise NotImplementedError("tickets  are immutable")
