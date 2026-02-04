from app.repositories.ticket_repository import create_ticket, get_ticket, get_tickets, update_ticket, get_classification_ticket
from app.services.category import get_categories_service
from app.services.priority import get_all_priorities
from app.repositories.prediction_log_repository import create_prediction_log
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.ticket import TicketCreateSchema, TicketUpdateSchema
from app.schemas.predictionLog import PredictionLogCreateSchema
from app.nlp.classifier import SemanticClassifier
from app.nlp.model import MODEL_NAME

async def create_ticket_service(db: AsyncSession, ticket_data: TicketCreateSchema, user_id: int):
    ticket = await create_ticket(db, ticket_data, user_id)

    # Texto para classificar
    text = f"{ticket.title}. {ticket.message}"

    #Categorias
    categories = await get_categories_service(db)

    confidence_category = None
    confidence_priority = None

    if categories:
        cat_options = [
            {
                "id": c.id,
                "name": c.category_name,
                "description": c.description or ""
            }
            for c in categories
        ]
        cat_best = SemanticClassifier.best_match(text,cat_options)
        category_id = cat_best["id"]
        confidence_category = cat_best.get("confidence")
    else:
        category_id = None

    #Prioridades
    priorities = await get_all_priorities(db)

    if priorities:
        prio_options  = [
            {
                "id": p.id,
                "name": p.priority_name,
                "description": f"level {p.level}"
            }
            for p in priorities
        ]
        prio_best  = SemanticClassifier.best_match(text,prio_options)
        priority_id  = prio_best["id"]
        confidence_priority = prio_best.get("confidence")
    else:
        priority_id = None

    #Atualizar o ticket com a classficação feita
    update_payload = TicketUpdateSchema(
        Categoryid=category_id,
        Priorityid=priority_id
    )

    ticket = await update_ticket(db, ticket.id, update_payload)

    log_payload = PredictionLogCreateSchema(
        ticket_id=ticket.id,
        input_text=text,
        predicted_category_id=category_id,
        predicted_priority_id=priority_id,
        confidence_category=confidence_category,
        confidence_priority=confidence_priority,
        model_name=MODEL_NAME,
    )
    await create_prediction_log(db, log_payload)

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
