from app.db.base import Base
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

class PredictionLog(Base):

    __tablename__ = "PredictionLog"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("Ticket.id"), nullable=True)
    ticket = relationship("Ticket")

    input_text = Column(String, index=True)
    predicted_category_id = Column(Integer, index=True, nullable=True)
    predicted_priority_id = Column(Integer, index=True, nullable=True)
    confidence_category = Column(Float, index=True, nullable=True)
    confidence_priority = Column(Float, index=True, nullable=True)
    model_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
