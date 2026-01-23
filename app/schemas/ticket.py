
import datetime
from pydantic import BaseModel, Field

class TicketCreateSchema(BaseModel):
    title: str = Field(..., example="Sample Ticket Title", max_length=255, min_length=5)
    message: str = Field(..., example="This is a sample ticket message.", min_length=10)

class TicketReadSchema(BaseModel):
    id: int
    title: str
    message: str
    priority: int | None = None
    status: str | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class TicketUpdateSchema(BaseModel):
    title: str | None = None
    message: str | None = None
    priority: int | None = None
    status: str | None = None
    category: str | None = None

class Config:
        from_attributes = True