

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreateSchema


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