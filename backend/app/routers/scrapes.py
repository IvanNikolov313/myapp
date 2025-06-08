from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from playwright.sync_api import sync_playwright
import re
import csv
from io import StringIO

from app.dependencies.db import get_db
from app.models.screener_config import ScreenerConfig
from app.models.company import Company
from app.models.scrape import Scrape
from app.models.executive import Executive  # Adjust if needed
from app.schemas.scrape import ScrapeOut

router = APIRouter(
    prefix="/scrapes",
    tags=["Scrapes"]
)

class ScrapeRunRequest(BaseModel):
    screener_config_id: int

def parse_market_cap_range(range_str: str):
    match = re.match(r'(\d+)([MB])-(\d+)([MB])', range_str.upper().replace('$', ''))
    if not match:
        raise ValueError("Invalid market cap format. Use like '100M-2B'.")
    def convert(value, unit):
        return int(value) * (1_000_000 if unit == 'M' else 1_000_000_000)
    return convert(match[1], match[2]), convert(match[3], match[4])

@router.post("/run")
def run_scrape(request: ScrapeRunRequest, db: Session = Depends(get_db)):
    config = db.query(ScreenerConfig).filter(ScreenerConfig.id == request.screener_config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Screener config not found")

    try:
        min_cap, max_cap = parse_market_cap_range(config.market_cap)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🌐 Navigating to Yahoo Screener...", flush=True)
        page.goto("https://finance.yahoo.com/research-hub/screener/equity/?start=0&count=100", timeout=60000)
        page.wait_for_selector('button:has-text("Market Cap")', timeout=15000)

        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path="/app/screenshots/before_filters_paginated.png")

        print("💰 Applying market cap filter...", flush=True)
        page.click('button:has-text("Market Cap")')
        page.click('label:has-text("Custom")')
        page.click('button:has-text("Between")')

        inputs = page.locator('input[placeholder*="e.g. 10M"]')
        inputs.nth(0).fill(str(min_cap))
        inputs.nth(1).fill(str(max_cap))
        page.click('button:has-text("Apply")')

        page.wait_for_timeout(3000)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path="/app/screenshots/filters_applied_paginated.png")

        companies = []
        page_number = 1

        while True:
            print(f"🔍 Scraping page {page_number}...", flush=True)
            page.wait_for_selector("table tbody tr", timeout=10000)
            rows = page.locator("table tbody tr")
            count = rows.count()

            for i in range(count):
                row = rows.nth(i)
                try:
                    name = row.locator("td").nth(2).locator("div").get_attribute("title") or ""
                    symbol = row.locator("td").nth(1).locator("span.symbol").inner_text().strip()
                    relative_link = row.locator("td").nth(1).locator("a").get_attribute("href")
                    profile_link = f"https://finance.yahoo.com{relative_link}" if relative_link else None
                    market_cap = row.locator("td").nth(9).inner_text().strip()

                    companies.append({
                        "name": name.strip(),
                        "symbol": symbol,
                        "profile_link": profile_link,
                        "market_cap": market_cap
                    })
                except Exception as e:
                    print(f"⚠️ Error parsing row {i} on page {page_number}: {e}", flush=True)
                    continue

            next_button = page.locator('button[data-testid="next-page-button"]')
            if next_button.is_disabled():
                print("⛔ Reached last page.", flush=True)
                break

            next_button.click()
            page_number += 1
            page.wait_for_timeout(2000)

        browser.close()

    print(f"✅ Scraped {len(companies)} companies across {page_number} pages. Comparing with DB...", flush=True)

    names = [c["name"] for c in companies if c["name"] and c["symbol"]]
    symbols = [c["symbol"] for c in companies if c["name"] and c["symbol"]]

    existing = db.query(Company).filter(
        Company.name.in_(names),
        Company.symbol.in_(symbols)
    ).all()

    existing_set = set((e.name, e.symbol) for e in existing)

    new_companies = [
        c for c in companies
        if (c["name"], c["symbol"]) not in existing_set
    ]

    print(f"🆕 Found {len(new_companies)} new companies to insert.", flush=True)

    try:
        scrape = Scrape(
            config_id=request.screener_config_id,
            total_companies=len(companies),
            new_companies=len(new_companies)
        )
        db.add(scrape)
        db.flush()

        for company in new_companies:
            db.add(Company(
                name=company["name"],
                symbol=company["symbol"],
                profile_link=company["profile_link"],
                market_cap=company["market_cap"],
                scrape_id=scrape.id
            ))

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {
        "message": (
            f"Scraping complete. {len(companies)} companies extracted. "
            f"{len(new_companies)} were new and saved."
        ),
        "scrape_id": scrape.id,
        "total_companies": len(companies),
        "new_companies_count": len(new_companies)
    }

@router.get("/", response_model=List[ScrapeOut])
def list_scrapes(db: Session = Depends(get_db)):
    return db.query(Scrape).order_by(Scrape.scraped_at.desc()).all()

@router.get("/{scrape_id}", response_model=ScrapeOut)
def get_scrape(scrape_id: int, db: Session = Depends(get_db)):
    scrape = db.query(Scrape).filter(Scrape.id == scrape_id).first()
    if not scrape:
        raise HTTPException(status_code=404, detail="Scrape not found")
    return scrape

@router.delete("/{scrape_id}")
def delete_scrape(scrape_id: int, db: Session = Depends(get_db)):
    scrape = db.query(Scrape).filter(Scrape.id == scrape_id).first()
    if not scrape:
        raise HTTPException(status_code=404, detail="Scrape not found")
    db.delete(scrape)
    db.commit()
    return {"message": f"Scrape {scrape_id} deleted."}

@router.get("/{scrape_id}/export-executives")
def export_executives(scrape_id: int, db: Session = Depends(get_db)):
    scrape = db.query(Scrape).filter(Scrape.id == scrape_id).first()
    if not scrape:
        raise HTTPException(status_code=404, detail="Scrape not found")

    companies = db.query(Company).filter(Company.scrape_id == scrape_id).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "name", "symbol", "profile_link", "marketCap",
        "sector", "industry", "employee_name", "employee_position", "Country"
    ])

    for company in companies:
        for exec in company.executives:
            position = "" if exec.name == "Missed Exec" else exec.position
            writer.writerow([
                company.name,
                company.symbol,
                company.profile_link,
                company.market_cap,
                company.sector or "",
                company.industry or "",
                exec.name,
                position,
                company.country or ""
            ])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=executives_scrape_{scrape_id}.csv"}
    )


@router.get("/{scrape_id}/export-companies")
def export_companies(scrape_id: int, db: Session = Depends(get_db)):
    scrape = db.query(Scrape).filter(Scrape.id == scrape_id).first()
    if not scrape:
        raise HTTPException(status_code=404, detail="Scrape not found")

    companies = db.query(Company).filter(Company.scrape_id == scrape_id).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "name", "symbol", "profile_link", "marketCap",
        "sector", "industry", "country"
    ])

    for company in companies:
        writer.writerow([
            company.name,
            company.symbol,
            company.profile_link,
            company.market_cap,
            company.sector or "",
            company.industry or "",
            company.country or ""
        ])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=companies_scrape_{scrape_id}.csv"}
    )
