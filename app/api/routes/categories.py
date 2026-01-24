from fastapi import APIRouter, Depends
from app.db.dependencies import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreateSchema, CategoryUpdateSchema
from app.services.category import create_category_service, delete_category_service, get_categories_service, get_category_service, update_category_service
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=Category, status_code=201)
async def create_category(
    category : CategoryCreateSchema, db: AsyncSession = Depends(get_db)
):
    return await create_category_service(db, category)

@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await get_category_service(db, category_id)

@router.get("/", response_model=list[Category])
async def list_all_categories(db: AsyncSession = Depends(get_db)):
    return await get_categories_service(db)

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_data : CategoryUpdateSchema, db: AsyncSession = Depends(get_db)
):
    return await update_category_service(db, category_data)

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    await delete_category_service(db, category_id)

