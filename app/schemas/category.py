import datetime
from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    category_name: str = Field(..., title="Category Name", max_length=100, min_length=2)
    description: str = Field(..., title="Description of category", max_length= 500, min_length=5)

class CategoryCreateSchema(CategoryBase):
    pass

class CategoryUpdateSchema(CategoryBase):
    pass

class CategorySchema(CategoryBase):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
