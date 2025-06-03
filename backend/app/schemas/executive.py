from pydantic import BaseModel

class ExecutiveBase(BaseModel):
    name: str
    position: str

class ExecutiveCreate(ExecutiveBase):
    company_id: int

class ExecutiveOut(ExecutiveBase):
    id: int

    class Config:
        orm_mode = True
