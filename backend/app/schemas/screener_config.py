from pydantic import BaseModel
from datetime import datetime

class ScreenerConfigBase(BaseModel):
    region: str
    market_cap: str
    label: str
    is_active: bool = True

class ScreenerConfigCreate(ScreenerConfigBase):
    pass

class ScreenerConfigOut(ScreenerConfigBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
