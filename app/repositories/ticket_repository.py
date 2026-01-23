

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreateSchema, TicketUpdateSchema


def create_ticket(db: Session, ticket: TicketCreateSchema) -> Ticket:
    db_ticket = Ticket(
        title=ticket.title,
        message=ticket.message,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int) -> Ticket:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def get_tickets(db: Session, skip: int = 0, limit: int = 100) -> list[Ticket]:
    return db.query(Ticket).offset(skip).limit(limit).all()

def update_ticket(db: Session, ticket_id: int, ticket: TicketUpdateSchema) -> Ticket:
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket:
        db_ticket.title = ticket.title
        db_ticket.message = ticket.message
        db_ticket.Priorityid = ticket.priority_id
        db_ticket.status = ticket.status
        db_ticket.Categoryid = ticket.category_id
        db_ticket.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_ticket)
    return db_ticket