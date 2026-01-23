from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "Ticket"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(String, index=True)
    status = Column(String, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    category_id = Column(Integer, ForeignKey("Category.id"), nullable=True)
    category = relationship("Category")

    priority_id = Column(Integer, ForeignKey("Priority.id"), nullable=True)
    priority = relationship("Priority")

    user_id = Column(Integer, ForeignKey("User.id"), nullable=True)
    user = relationship("User")