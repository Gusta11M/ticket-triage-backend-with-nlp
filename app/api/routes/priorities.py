from fastapi import APIRouter, Depends, HTTPException
from app.db.dependencies import get_db
from app.schemas.priority import PriorityCreateSchema, PriorityUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.priority import create_priority_service, delete_priority_service, delete_priority_service, get_priorities_service, get_priority_service, update_priority_service


router = APIRouter(prefix="/priorities", tags=["Priorities"])

@router.post(
    "/", 
    status_code=201, 
    summary="Registar nível de prioridade",
    description="Define um novo nível de prioridade (ex: Crítico, Urgente)."
)
async def create_priority(priority: PriorityCreateSchema, db: AsyncSession = Depends(get_db)):
    return await create_priority_service(db, priority)

@router.get(
    "/{priority_id}", 
    summary="Obter detalhes da prioridade",
    responses={404: {"description": "Prioridade não encontrada"}}
)
async def get_priority(priority_id: int, db: AsyncSession = Depends(get_db)):
    result = await get_priority_service(db, priority_id)
    if not result:
        raise HTTPException(status_code=404, detail="Priority not found")
    return result

@router.get("/", summary="Listar prioridades")
async def get_priorities(db: AsyncSession = Depends(get_db)):
    return await get_priorities_service(db)

@router.put("/{priority_id}", summary="Modificar prioridade")
async def update_priority(priority_id: int, priority: PriorityUpdateSchema, db: AsyncSession = Depends(get_db)):
    return await update_priority_service(db, priority_id, priority)

@router.delete("/{priority_id}", status_code=204, summary="Apagar prioridade")
async def delete_priority(priority_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_priority_service(db, priority_id)


