
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.db.base import Base

class Category (Base):
    
    __tablename__ = "Category"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)