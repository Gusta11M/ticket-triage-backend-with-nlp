
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import router
from app.db.dependencies import get_db
from app.schemas.ticket import TicketCreateSchema, TicketReadSchema
from app.services.ticket import create_ticket_service


router = APIRouter()

@router.post("/tickets", response_model=TicketReadSchema)
def create_ticket(
    ticket: TicketCreateSchema, db: Session = Depends(get_db)
):
    return create_ticket_service(db, ticket)