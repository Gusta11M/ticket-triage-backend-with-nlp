from fastapi import APIRouter, Depends, HTTPException
from app.db.dependencies import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema
from app.services.category import create_category_service, delete_category_service, get_categories_service, get_category_service, update_category_service
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post(
    "/", 
    response_model=CategorySchema, 
    status_code=201,
    summary="Criar nova categoria",
    description="Regista uma nova categoria temática para classificação de tickets."
)
async def create_category(category: CategoryCreateSchema, db: AsyncSession = Depends(get_db)):
    """Cria uma categoria no banco de dados e retorna o objeto criado."""
    return await create_category_service(db, category)

@router.get(
    "/{category_id}", 
    response_model=CategorySchema,
    summary="Obter categoria por ID",
    responses={404: {"description": "Categoria não encontrada"}}
)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Procura uma categoria específica pelo seu ID único."""
    category = await get_category_service(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get(
    "/", 
    response_model=list[CategorySchema],
    summary="Listar todas as categorias",
    description="Retorna uma lista completa de todas as categorias registadas."
)
async def list_all_categories(db: AsyncSession = Depends(get_db)):
    return await get_categories_service(db)

@router.put(
    "/{category_id}", 
    response_model=CategorySchema,
    summary="Atualizar categoria",
    responses={404: {"description": "Categoria não encontrada"}}
)
async def update_category(
    category_id: int, category_data: CategoryUpdateSchema, db: AsyncSession = Depends(get_db)
):
    """Atualiza os campos de uma categoria existente (ex: nome)."""
    return await update_category_service(db, category_id, category_data)

@router.delete(
    "/{category_id}", 
    status_code=204,
    summary="Remover categoria"
)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Remove permanentemente uma categoria do sistema."""
    await delete_category_service(db, category_id)

