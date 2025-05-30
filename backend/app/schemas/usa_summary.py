# app/schemas/usa_summary.py
from pydantic import BaseModel

class USAMasterSummary(BaseModel):
    companies: int
    employees: int

class USAScrapeSummary(BaseModel):
    id: int
    name: str
    total_companies: int
    total_employees: int
