from datetime import datetime
from sqlalchemy import select
from app.models.priority import Priority
from app.schemas.priority import PriorityCreateSchema, PrioritySchema, PriorityUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession

async def create_priority(db: AsyncSession, priority: PriorityCreateSchema) -> PrioritySchema:

    db_priority = Priority(
        priority_name=priority.priority_name,
        level=priority.level,
        created_at=datetime.utcnow()
    )

    db.add(db_priority)
    await db.commit()
    await db.refresh(db_priority)
    return db_priority

async def get_priority_by_id(db: AsyncSession, priority_id: int) -> PrioritySchema | None:

    result = await db.execute(
        select(Priority).where(Priority.id == priority_id)
    )

    return result.scalars().first()

async def get_all_priorities(db: AsyncSession) -> list[PrioritySchema]:
    result = await db.execute(
        select(Priority)
    )
    return result.scalars().all()

async def update_priority(db: AsyncSession, priority_id: int, priority_data: PriorityUpdateSchema) -> PrioritySchema | None:

    db_priority = await get_priority_by_id(db, priority_id)
    
    if not db_priority:
        return None

    updated_data = priority_data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(db_priority, key, value)
    
    await db.commit()
    await db.refresh(db_priority)

    return db_priority

async def delete_priority(db: AsyncSession, priority_id: int) -> bool:

    db_priority = await get_priority_by_id(db, priority_id)
    if not db_priority:
        return False

    await db.delete(db_priority)
    await db.commit()
    return True