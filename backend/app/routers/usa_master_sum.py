from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.responses import JSONResponse

from app.dependencies.db import get_db
from app.models.company import Company
from app.models.executive import Executive
from app.models.scrape import Scrape
from app.schemas.usa_summary import USAMasterSummary, USAScrapeSummary

router = APIRouter()

@router.get("/usa/master-summary", response_model=USAMasterSummary)
def usa_master_sum(db: Session = Depends(get_db)):
    total_companies = db.query(Company).count()
    return JSONResponse(
        content={"companies": total_companies, "employees": 0},
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )

@router.get("/usa/scrapes-summary", response_model=list[USAScrapeSummary])
def usa_scrapes_sum(db: Session = Depends(get_db)):
    scrapes_data = db.query(
        Scrape.id,
        Scrape.scraped_at.label("scraped_at"),
        Scrape.total_companies,
        Scrape.new_companies
    ).order_by(Scrape.scraped_at.desc()).all()

    result = []
    for s in scrapes_data:
        companies_scraped = db.query(Company.id).filter(
            Company.scrape_id == s.id
        ).filter(
            db.query(Executive.id).filter(Executive.company_id == Company.id).exists()
        ).count()

        executive_count = db.query(Executive).join(Company).filter(
            Company.scrape_id == s.id
        ).count()

        result.append({
            "id": s.id,
            "name": f"Scrape - {s.scraped_at.strftime('%Y-%m-%d %H:%M')}",
            "created_at": s.scraped_at.isoformat(),
            "unique_companies": s.new_companies,
            "total_scraped": s.total_companies,
            "companies_scraped": companies_scraped,
            "executive_count": executive_count,
        })

    return result
