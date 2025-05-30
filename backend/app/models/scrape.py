from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.screener_config import ScreenerConfig

class Scrape(Base):
    __tablename__ = "scrape"
    id = Column(Integer, primary_key=True, index=True)
    config_id = Column(Integer, ForeignKey("screenerconfig.id"), nullable=False)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())

    total_companies = Column(Integer, nullable=False, default=0)
    new_companies = Column(Integer, nullable=False, default=0)

    companies = relationship("Company", back_populates="scrape")
