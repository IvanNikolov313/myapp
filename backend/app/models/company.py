from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    scrape_id = Column(Integer, ForeignKey("scrape.id"), nullable=True)
    name = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    profile_link = Column(String, nullable=True)
    market_cap = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    website = Column(String, nullable=True)
    country = Column(String, nullable=True)
