from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from app.db.session import Base

class Priority (Base):
    __tablename__ = "Priority"

    id = Column(Integer, primary_key=True, index=True)
    priority_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)