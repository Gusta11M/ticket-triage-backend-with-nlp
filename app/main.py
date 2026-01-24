from fastapi import FastAPI
from app.api.router import api_router
from app.db.session import Base, engine
from app.models import category, priority, user, ticket

app = FastAPI()

@app.on_event("startup")
def starup():
    Base.metadata.create_all(bind=engine)

app.include_router(api_router)