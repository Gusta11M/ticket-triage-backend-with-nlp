from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, role_required
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.ticket import TicketResponseSchema,TicketCreateSchema, TicketUpdateSchema, TicketResponseClassificationSchema
from app.services.ticket import (
    create_ticket_service, 
    get_ticket_service, 
    get_tickets_service, 
    update_ticket_service,
    get_classification_ticket_service
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post(
    "/", 
    response_model=TicketResponseSchema, 
    status_code=201,
    summary="Abrir novo Ticket",
    description="Cria um ticket no sistema. A prioridade e categoria podem ser atribuídas manualmente ou via NLP."
)
async def create_ticket(ticket: TicketCreateSchema, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_ticket_service(db, ticket, current_user.id)

@router.get(
    "/{ticket_id}", 
    response_model=TicketResponseSchema,
    summary="Consultar Ticket específico",
    responses={404: {"description": "O ticket solicitado não existe."}}
)
async def read_ticket(ticket_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(role_required("admin"))):
    ticket = await get_ticket_service(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get(
    "/", 
    response_model=list[TicketResponseSchema],
    summary="Listagem paginada de Tickets",
    description="Recupera tickets com suporte a paginação via parâmetros 'skip' e 'limit'."
)
async def read_tickets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(role_required("admin"))):
    return await get_tickets_service(db, skip, limit)

@router.get(
        "/classification/{ticket_id}",
        response_model=TicketResponseClassificationSchema,
        summary = "Devolve a categoria e a prioridade de um ticket específico",
        description= "Permite obter a categoria e a prioridade de um ticket"
)
async def get_classification_ticket(ticket_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_classification_ticket_service(db, ticket_id)


@router.put(
    "/{ticket_id}", 
    response_model=TicketResponseSchema,
    summary="Atualizar dados do Ticket",
    description="Permite alterar o status, mensagem, ou reclassificar o ticket."
)
async def update_ticket(ticket_id: int, ticket: TicketUpdateSchema, db: AsyncSession = Depends(get_db), current_user: User = Depends(role_required("admin"))):
    updated_ticket = await update_ticket_service(db, ticket_id, ticket)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated_ticket