from app.repositories.ticket_repository import create_ticket, get_ticket, get_tickets, update_ticket
from sqlalchemy.orm import Session

def create_ticket_service(db : Session, ticket_data) :

    ticket = create_ticket(db, ticket_data)

    return ticket

def get_ticket_service(db : Session, ticket_id : int) :

    ticket = get_ticket(db, ticket_id)

    return ticket


def get_tickets_service(db : Session, skip : int = 0, limit : int = 100) :

    tickets = get_tickets(db, skip, limit)

    return tickets

def update_ticket_service(db : Session, ticket_id : int, ticket_data) :

    ticket = update_ticket(db, ticket_id, ticket_data)

    return ticket
