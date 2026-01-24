
import datetime
from pydantic import BaseModel, Field

from app.models.ticketStatus import TicketStatus

class TicketCreateSchema(BaseModel):
    title: str = Field(..., example="Sample Ticket Title", max_length=255, min_length=5)
    message: str = Field(..., example="This is a sample ticket message.", min_length=10)

class TicketUpdateSchema(BaseModel):
    title: str | None = None
    message: str | None = None
    priority_id: int | None = None
    status: str | None = None
    category_id: int | None = None

class Config:
        from_attributes = True