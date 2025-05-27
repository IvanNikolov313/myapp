from pydantic import BaseModel
from datetime import datetime

class ScrapeCreate(BaseModel):
    config_id: int
    total_companies: int
    new_companies: int

class ScrapeOut(BaseModel):
    id: int
    config_id: int
    scraped_at: datetime
    total_companies: int
    new_companies: int

    class Config:
        orm_mode = True
