from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base  # ← this is your custom base class

class ScreenerConfig(Base):
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, nullable=False)
    market_cap = Column(String, nullable=False)
    label = Column(String, unique=False, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
