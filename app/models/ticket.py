from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.db.session import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(String, index=True)
    status = Column(String, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)