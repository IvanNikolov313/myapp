from pydantic import BaseModel

class USAMasterSummary(BaseModel):
    companies: int
    employees: int

class USAScrapeSummary(BaseModel):
    id: int
    name: str
    created_at: str
    unique_companies: int  # <-- formerly new_companies
    total_scraped: int     # <-- formerly total_companies
    companies_scraped: int
    executive_count: int
