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

    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    db_ticket = result.scalars().first()
    
    if db_ticket:
        db_ticket.title = ticket.title
        db_ticket.message = ticket.message
        db_ticket.Priorityid = ticket.priority_id
        db_ticket.status = ticket.status
        db_ticket.Categoryid = ticket.category_id
        db_ticket.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(db_ticket)
    return db_ticket