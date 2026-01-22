from fastapi import FastAPI
from app.api.routes import tickets
from app.db.session import Base, engine
from app.models.ticket import Ticket

app = FastAPI()

@app.on_event("startup")
def starup():
    Base.metadata.create_all(bind=engine)

    
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])