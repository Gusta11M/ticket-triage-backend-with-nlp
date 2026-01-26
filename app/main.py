from fastapi import FastAPI
from app.api.router import api_router

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

app.include_router(api_router)