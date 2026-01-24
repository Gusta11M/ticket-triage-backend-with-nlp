from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket import Ticket
from app.models.ticketStatus import TicketStatus
from app.schemas.ticket import TicketCreateSchema, TicketUpdateSchema

async def create_ticket(db: AsyncSession, ticket: TicketCreateSchema) -> Ticket:
    db_ticket = Ticket(
        title=ticket.title,
        message=ticket.message,
        status=TicketStatus.OPEN.value,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def get_ticket(db: AsyncSession, ticket_id: int) -> Ticket:
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalars().first()

async def get_tickets(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Ticket]:
    result = await db.execute(select(Ticket).offset(skip).limit(limit))
    return result.scalars().all()

async def update_ticket(db: AsyncSession, ticket_id: int, ticket: TicketUpdateSchema) -> Ticket:

    db_ticket = await get_ticket(db, ticket_id)

    if db_ticket is None:
        return None
    
    update_data = ticket.model_dump(exclude_unset=True)

    # 3. Atualiza apenas os atributos presentes no dicionário
    for key, value in update_data.items():
        setattr(db_ticket, key, value)

    # 4. Atualiza sempre o timestamp de modificação
    db_ticket.updated_at = datetime.utcnow()
        
    await db.commit()
    await db.refresh(db_ticket)

    return db_ticket