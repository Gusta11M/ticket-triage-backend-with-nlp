from fastapi import APIRouter
from app.api.routes import categories, tickets

api_router = APIRouter()

api_router.include_router(tickets.router)
api_router.include_router(categories.router)