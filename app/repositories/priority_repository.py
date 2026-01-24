from datetime import datetime
from sqlalchemy import select
from app.models.priority import Priority
from app.schemas.priority import PriorityCreateSchema, PriorityUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession

async def create_priority(db: AsyncSession, priority: PriorityCreateSchema) -> Priority:

    db_priority = Priority(
        priority_name=priority.priority_name,
        created_at=datetime.utcnow()
    )

    db.add(db_priority)
    await db.commit()
    await db.refresh(db_priority)
    return db_priority

async def get_priority_by_id(db: AsyncSession, priority_id: int) -> Priority | None:

    result = await db.execute(
        select(Priority).where(Priority.id == priority_id)
    )

    return result.scalars().first()

async def get_all_priorities(db: AsyncSession) -> list[Priority]:
    result = await db.execute(
        select(Priority)
    )
    return result.scalars().all()

async def update_priority(db: AsyncSession, priority_id: int, priority_data: PriorityUpdateSchema) -> Priority | None:

    db_priority = await get_priority_by_id(db, priority_id)
    
    if not db_priority:
        return None

    db_priority.priority_name = priority_data.priority_name
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