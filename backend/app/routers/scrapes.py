from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.models.screener_config import ScreenerConfig
from playwright.sync_api import sync_playwright
import re
import time

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

        print("🌐 Navigating to Yahoo Screener with 100 results per page...")
        page.goto("https://finance.yahoo.com/research-hub/screener/equity/?start=0&count=100")
        page.wait_for_selector('button:has-text("Market Cap")', timeout=15000)

        print("📸 Screenshot: Before filters")
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path="/app/screenshots/before_filters.png")

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
        page.screenshot(path="/app/screenshots/filters_applied.png")

        next_button = page.locator('button[data-testid="next-page-button"]')
        click_count = 0

        print("⏭️ Clicking next page until the last page...")
        while True:
            if next_button.is_disabled():
                print("⛔ Last page reached.")
                break

            if click_count == 0:
                page.wait_for_timeout(1500)
                page.screenshot(path="/app/screenshots/after_first_next.png")

            next_button.click()
            click_count += 1
            page.wait_for_timeout(1500)
            next_button = page.locator('button[data-testid="next-page-button"]')

        print(f"📸 Screenshot: Final page after {click_count} nexts")
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path="/app/screenshots/final_page.png")

        browser.close()

    return {"message": f"Scraping complete. Clicked next {click_count} times."}
