from app.repositories.ticket_repository import create_ticket, get_ticket, get_tickets, update_ticket, get_classification_ticket
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.ticket import TicketCreateSchema, TicketUpdateSchema

async def create_ticket_service(db: AsyncSession, ticket_data: TicketCreateSchema, user_id: int):
    ticket = await create_ticket(db, ticket_data, user_id)
    return ticket

async def get_ticket_service(db: AsyncSession, ticket_id: int):
    ticket = await get_ticket(db, ticket_id)
    return ticket

async def get_tickets_service(db: AsyncSession, skip: int = 0, limit: int = 100):
    tickets = await get_tickets(db, skip, limit)
    return tickets

async def get_classification_ticket_service(db: AsyncSession, ticket_id: int):
    classification_ticket = await get_classification_ticket(db, ticket_id)
    return classification_ticket

async def update_ticket_service(db: AsyncSession, ticket_id: int, ticket_data: TicketUpdateSchema):
    ticket = await update_ticket(db, ticket_id, ticket_data)
    return ticket