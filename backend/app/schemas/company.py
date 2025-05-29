from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    symbol: str
    profile_link: str
    market_cap: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None        # ✅ New field
    scrape_id: Optional[int] = None      # ✅ Optional foreign key for scrape

class Company(CompanyCreate):
    id: int

    class Config:
        orm_mode = True
