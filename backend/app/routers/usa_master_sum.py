from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.company import Company
from app.models.scrape import Scrape
from app.schemas.usa_summary import USAMasterSummary, USAScrapeSummary  # <-- import your schemas

router = APIRouter()

from fastapi.responses import JSONResponse

@router.get("/usa/master-summary", response_model=USAMasterSummary)
def usa_master_sum(db: Session = Depends(get_db)):
    total_companies = db.query(Company).count()
    total_employees = 0
    data = {"companies": total_companies, "employees": total_employees}
    return JSONResponse(content=data, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@router.get("/usa/scrapes-summary", response_model=list[USAScrapeSummary])
def usa_scrapes_sum(db: Session = Depends(get_db)):
    scrapes_data = db.query(
        Scrape.id,
        Scrape.scraped_at.label("scraped_at"),
        Scrape.total_companies,
        Scrape.new_companies.label("total_employees"),
    ).order_by(Scrape.scraped_at.desc()).all()

    result = [
        {
            "id": s.id,
            "name": f"Scrape - {s.scraped_at.strftime('%Y-%m-%d %H:%M')}",
            "total_companies": s.total_companies,
            "total_employees": s.total_employees,
        }
        for s in scrapes_data
    ]
    return result


