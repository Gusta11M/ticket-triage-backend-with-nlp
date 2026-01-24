from fastapi import APIRouter, Depends, HTTPException
from app.db.dependencies import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema
from app.services.category import create_category_service, delete_category_service, get_categories_service, get_category_service, update_category_service
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategorySchema, status_code=201)
async def create_category(
    category : CategoryCreateSchema, db: AsyncSession = Depends(get_db)
):
    return await create_category_service(db, category)

@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await get_category_service(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=list[CategorySchema])
async def list_all_categories(db: AsyncSession = Depends(get_db)):
    return await get_categories_service(db)

@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int, category_data : CategoryUpdateSchema, db: AsyncSession = Depends(get_db)
):
    return await update_category_service(db, category_id, category_data)

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    await delete_category_service(db, category_id)

