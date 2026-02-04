import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.ticketStatus import TicketStatus

class TicketBase(BaseModel):
    title: str = Field(..., example="Sample Ticket Title", max_length=255, min_length=5)
    message: str = Field(..., example="This is a sample ticket message.", min_length=10)

class TicketCreateSchema(TicketBase):
    """Schema para criação de ticket - user_id é extraído do token JWT"""
    pass

class TicketResponseSchema(TicketBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    Priorityid: int | None = None
    status: TicketStatus
    Categoryid: int | None = None
    Userid: int | None = None
    
    model_config = ConfigDict(from_attributes=True)

class TicketResponseClassificationSchema(BaseModel):
    id: int = Field(...)
    category: str | None = None
    priority: int | None = None

class TicketUpdateSchema(BaseModel):
    title: str | None = Field(None, example="Updated Ticket Title", max_length=255, min_length=5)
    message: str | None = Field(None, example="This is an updated ticket message.", min_length=10)
    Priorityid: int | None = Field(None, example=2)
    status: TicketStatus | None = Field(None, example=TicketStatus.IN_PROGRESS)
    Categoryid: int | None = Field(None, example=3)
    
    model_config = ConfigDict(from_attributes=True)