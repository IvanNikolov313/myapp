from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Executive(Base):
    __tablename__ = "executives"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    
    company = relationship("Company", back_populates="executives")
