
from app.repositories.ticket_repository import create_ticket
from sqlalchemy.orm import Session

def create_ticket_service(db : Session, ticket_data) :

    ticket = create_ticket(db, ticket_data)

    return ticket

