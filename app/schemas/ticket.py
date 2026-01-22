
import datetime
from pydantic import BaseModel

class TicketCreateSchema(BaseModel):
    title: str
    message: str

class TicketReadSchema(BaseModel):
    id: int
    title: str
    message: str
    priority: int
    status: str
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