from fastapi import APIRouter
from app.api.routes import categories, tickets, priorities, auth

api_router = APIRouter()

api_router.include_router(tickets.router)
api_router.include_router(categories.router)
api_router.include_router(priorities.router)
api_router.include_router(auth.router)