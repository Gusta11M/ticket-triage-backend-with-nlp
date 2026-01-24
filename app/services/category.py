
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.repositories.category_repository import (
    create_category,
    get_category_by_id,
    get_all_categories,
    update_category,
    delete_category
)

from app.schemas.category import CategoryCreateSchema, CategoryUpdateSchema

async def create_category_service(db: AsyncSession, category: CategoryCreateSchema) -> Category:
    category_obj = await create_category(db, category)
    return category_obj

async def get_category_service(db: AsyncSession, category_id: int) -> Category | None:
    category_obj = await get_category_by_id(db, category_id)
    return category_obj

async def get_categories_service(db: AsyncSession) -> list[Category]:
    categories = await get_all_categories(db)
    return categories

async def update_category_service(db: AsyncSession, category_data : CategoryUpdateSchema) -> Category | None:
    category_obj = await update_category(db, category_data)
    return category_obj

async def delete_category_service(db: AsyncSession, category_id: int) -> bool:
    confirmation = await delete_category(db, category_id)
    return confirmation