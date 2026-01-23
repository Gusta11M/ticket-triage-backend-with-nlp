from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship
from app.models.ticketStatus import TicketStatus


class Ticket(Base):
    __tablename__ = "Ticket"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(String, index=True)
    status = Column(String, index=True, default=TicketStatus.OPEN.value)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    Categoryid = Column(Integer, ForeignKey("Category.id"), nullable=True)
    category = relationship("Category")

    Priorityid = Column(Integer, ForeignKey("Priority.id"), nullable=True)
    priority = relationship("Priority")

    Userid = Column(Integer, ForeignKey("User.id"), nullable=True)
    user = relationship("User")