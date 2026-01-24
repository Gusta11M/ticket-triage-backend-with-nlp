from fastapi import FastAPI
from app.api.router import api_router
from app.db.session import Base, engine
from app.models import category, priority, user, ticket

app = FastAPI(
    title="Ticket Triage NLP API",
    description="""
    API para gestão e triagem automática de tickets utilizando Processamento de Linguagem Natural.
    
    ## Funcionalidades
    * **Tickets**: Criação e gestão de incidentes.
    * **Categories**: Organização temática.
    * **Priorities**: Definição de níveis de prioridade.
    * **NLP Triage**: Classificação automática de prioridade (em breve).
    """,
    version="1.0.0",
    contact={
        "name": "Gustavo Daniel Loureiro Marques",
        "email": "gustadaniel.marques@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

@app.on_event("startup")
async def starup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)