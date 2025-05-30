from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.scrape import Scrape
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    scrape_id = Column(Integer, ForeignKey("scrape.id"), nullable=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    profile_link = Column(String, nullable=True)
    market_cap = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    website = Column(String, nullable=True)
    country = Column(String, nullable=True)

    scrape = relationship("Scrape", back_populates="companies")
