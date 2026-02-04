import datetime
from pydantic import BaseModel, ConfigDict, Field

class PredictionLogBase(BaseModel):
    pass

class PredictionLogCreateSchema(PredictionLogBase):
    ticket_id: int | None = None
    input_text: str = Field(...)
    predicted_category_id: int | None = None
    predicted_priority_id: int | None = None
    confidence_category: float | None = None
    confidence_priority: float | None = None
    model_name: str | None = None

class PredictionLogResponseSchema(PredictionLogBase):
    id: int
    ticket_id: int | None = None
    input_text: str
    predicted_category_id: int | None = None
    predicted_priority_id: int | None = None
    confidence_category: float | None = None
    confidence_priority: float | None = None
    model_name: str | None = None
    created_at: datetime.datetime | None = None

    model_config = ConfigDict(from_attributes=True)
