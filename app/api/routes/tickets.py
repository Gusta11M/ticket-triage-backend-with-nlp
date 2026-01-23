from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db
from app.schemas.ticket import TicketCreateSchema, TicketReadSchema, TicketUpdateSchema
from app.services.ticket import (
    create_ticket_service, 
    get_ticket_service, 
    get_tickets_service, 
    update_ticket_service
)

router = APIRouter(prefix="/tickets")

@router.post("/", response_model=TicketReadSchema, status_code=201)
async def create_ticket(
    ticket: TicketCreateSchema, db: AsyncSession = Depends(get_db)
):
    return await create_ticket_service(db, ticket)

@router.get("/{ticket_id}", response_model=TicketReadSchema)
async def read_ticket(
    ticket_id: int, db: AsyncSession = Depends(get_db)
):
    ticket = await get_ticket_service(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/", response_model=list[TicketReadSchema])
async def read_tickets(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await get_tickets_service(db, skip, limit)

@router.put("/{ticket_id}", response_model=TicketReadSchema)
async def update_ticket(
    ticket_id: int,
    ticket: TicketUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    updated_ticket = await update_ticket_service(db, ticket_id, ticket)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated_ticket