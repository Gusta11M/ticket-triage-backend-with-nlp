from app.models.priority import Priority
from app.schemas.priority import PriorityCreateSchema, PrioritySchema
from app.repositories.priority_repository import create_priority, delete_priority, get_priority_by_id, get_all_priorities, update_priority
from sqlalchemy.ext.asyncio import AsyncSession

async def create_priority_service(db:AsyncSession, priority:PriorityCreateSchema) -> PrioritySchema:
    priority_obj = await create_priority(db, priority)
    return priority_obj

async def get_priority_service(db:AsyncSession, priority_id:int) -> PrioritySchema | None:
    priority_obj = await get_priority_by_id(db, priority_id)
    return priority_obj

async def get_priorities_service(db:AsyncSession) -> list[Priority]:
    priorities = await get_all_priorities(db)
    return priorities

async def update_priority_service(db:AsyncSession, priority_id:int, priority_data:PriorityCreateSchema) -> PrioritySchema | None:
    priority_obj = await update_priority(db, priority_id, priority_data)
    return priority_obj

async def delete_priority_service(db:AsyncSession, priority_id:int) -> bool:
    confirmation = await delete_priority(db, priority_id)
    return confirmation
