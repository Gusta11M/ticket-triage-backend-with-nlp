from fastapi import FastAPI
from app.api.router import api_router
from app.db.session import Base, engine
from app.models import category, priority, user, ticket

app = FastAPI()

@app.on_event("startup")
async def starup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)