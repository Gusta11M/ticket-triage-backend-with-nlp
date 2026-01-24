from pydantic import ConfigDict, Field

class PriorityBase:
    priority_name: str = Field(..., example="High", min_length=1, max_length=50)
    level: int = Field(..., example=3, ge=1, le=5)

class PriorityCreateSchema(PriorityBase):
    pass

class PriorityUpdateSchema(PriorityBase):
    pass

class PrioritySchema(PriorityBase):
    id: int = Field(..., example=1)
    created_at: str = Field(..., example="2024-01-01T12:00:00Z")

model_config = ConfigDict(from_attributes=True)