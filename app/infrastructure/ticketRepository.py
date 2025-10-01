from typing import Optional
from pydantic import BaseModel

from app.infrastructure.baseRepository import BaseRepository
from app.infrastructure.models import TicketORM


class CreateTicketSchema(BaseModel):
    ticket_number: str
    order_id: int
    passenger_id: int


class UpdateTicketSchema(BaseModel):
    ticket_number: Optional[str] = None
    order_id: Optional[int] = None
    passenger_id: Optional[int] = None


class TicketRepository(
    BaseRepository[TicketORM, CreateTicketSchema, UpdateTicketSchema]
):
    def update(self, *args, **kwargs):
        raise NotImplementedError("tickets  are immutable")
