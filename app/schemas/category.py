import datetime
from pydantic import Field


class CategoryCreateSchema:
    category_name: str = Field(..., example="Software Issue", max_length=100, min_length=3)

class CategoryUpdateSchema:
    id: int
    category_name: str | None = None

class Config:
        from_attributes = True