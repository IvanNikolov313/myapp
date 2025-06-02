from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.models.screener_config import ScreenerConfig
from playwright.sync_api import sync_playwright
import re

router = APIRouter()

class ScrapeRunRequest(BaseModel):
    screener_config_id: int

def parse_market_cap_range(range_str: str):
    match = re.match(r'(\d+)([MB])-(\d+)([MB])', range_str.upper().replace('$', ''))
    if not match:
        raise ValueError("Invalid market cap format. Use like '100M-2B'.")

    def convert(value, unit):
        return int(value) * (1_000_000 if unit == 'M' else 1_000_000_000)

    return convert(match[1], match[2]), convert(match[3], match[4])

@router.post("/scrapes/run")
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

        print("🌐 Navigating to Yahoo Screener...")
        page.goto("https://finance.yahoo.com/research-hub/screener/equity/?start=0&count=100")
        page.wait_for_selector('button:has-text("Market Cap")', timeout=15000)

        print("📸 Screenshot: Before filters")
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path="/app/screenshots/before_filters_paginated.png")

        print("💰 Applying market cap filter...")
        page.click('button:has-text("Market Cap")')
        page.click('label:has-text("Custom")')
        page.click('button:has-text("Between")')

        inputs = page.locator('input[placeholder*="e.g. 10M"]')
        inputs.nth(0).fill(str(min_cap))
        inputs.nth(1).fill(str(max_cap))
        page.click('button:has-text("Apply")')

        print("📸 Screenshot: Filters applied")
        page.wait_for_timeout(3000)
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path="/app/screenshots/filters_applied_paginated.png")

        companies = []
        page_number = 1

        while True:
            print(f"🔍 Scraping page {page_number}...")
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
                    print(f"⚠️ Error parsing row {i} on page {page_number}: {e}")
                    continue

            next_button = page.locator('button[data-testid="next-page-button"]')
            if next_button.is_disabled():
                print("⛔ Reached last page.")
                break

            print("⏭️ Clicking next...")
            next_button.click()
            page_number += 1
            page.wait_for_timeout(2000)

        browser.close()

        return {
            "message": f"Scraping complete. {len(companies)} companies extracted from {page_number} page(s).",
            "companies": companies
        }
