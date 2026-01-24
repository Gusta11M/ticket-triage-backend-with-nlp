import datetime
from pydantic import Field


class CategoryCreateSchema:
    category_name: str = Field(..., example="Software Issue", max_length=100, min_length=3)

class CategoryReadSchema:
    id: int
    category_name: str
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }

class CategoryUpdateSchema:
    id: int
    category_name: str | None = None

class CategoryDeleteSchema:
    id: int

class Config:
        from_attributes = True