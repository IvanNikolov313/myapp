from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.models.company import Company
from app.models.executive import Executive
from app.schemas.executive import ExecutiveOut
from typing import List
import time
import re
from playwright.sync_api import sync_playwright

router = APIRouter(
    prefix="/executives",
    tags=["Executives"]
)

allowed_title_patterns = [
    r"\bchief executive officer\b",
    r"\bceo\b",
    r"\bchief financial officer\b",
    r"\bcfo\b",
]

def title_allowed(title: str) -> bool:
    title = title.lower()
    if any(re.search(pattern, title) for pattern in allowed_title_patterns):
        return True
    if "investor" in title:
        return True
    return False

@router.post("/scrape/{scrape_id}")
def scrape_executives(scrape_id: int, db: Session = Depends(get_db)):
    exec_subquery = db.query(Executive.company_id).subquery()

    companies = (
        db.query(Company)
        .filter(Company.scrape_id == scrape_id)
        .filter(~Company.id.in_(exec_subquery))
        .all()
    )

    if not companies:
        total_companies = db.query(Company).filter(Company.scrape_id == scrape_id).count()
        already_scraped = db.query(Executive.company_id).join(Company).filter(Company.scrape_id == scrape_id).distinct().count()
        return {
            "message": f"All executives already scraped for scrape ID {scrape_id}. "
                       f"{already_scraped} / {total_companies} companies already processed."
        }

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for idx, company in enumerate(companies, start=1):
            print(f"Scraping company {idx}: {company.name}", flush=True)

            if not company.profile_link:
                dummy_exec = Executive(
                    company_id=company.id,
                    name="Missed Exec",
                    position="Miss: No profile link"
                )
                db.add(dummy_exec)
                db.commit()
                results.append({
                    "company_id": company.id,
                    "name": company.name,
                    "profile_link": company.profile_link,
                    "country": "No profile link",
                    "sector": None,
                    "industry": None,
                    "website": None,
                    "executives": [],
                    "error": "Miss: No profile link"
                })
                continue

            try:
                profile_url = company.profile_link.rstrip('/') + "/profile"
                page.goto(profile_url)
                page.wait_for_selector(".address", timeout=7000)

                page_content = page.content()
                if "Profile Information Not Available" in page_content:
                    dummy_exec = Executive(
                        company_id=company.id,
                        name="Missed Exec",
                        position="Miss: Profile info unavailable"
                    )
                    db.add(dummy_exec)
                    db.commit()
                    results.append({
                        "company_id": company.id,
                        "name": company.name,
                        "profile_link": company.profile_link,
                        "country": "Profile Info Unavailable",
                        "sector": None,
                        "industry": None,
                        "website": None,
                        "executives": [],
                        "error": "Miss: Profile info unavailable"
                    })
                    continue

                address_element = page.query_selector(".address")
                if address_element:
                    divs = address_element.query_selector_all("div")
                    country = divs[-1].inner_text().strip() if divs else "Profile Info Unavailable"
                else:
                    country = "Profile Info Unavailable"

                sector_element = page.query_selector("dl.company-stats > div:nth-child(1) dd a")
                sector = sector_element.inner_text().strip() if sector_element else None

                industry_element = page.query_selector("dl.company-stats > div:nth-child(2) a")
                industry = industry_element.inner_text().strip() if industry_element else None

                website_element = page.query_selector('a.primary-link[href^="http"]')
                website = website_element.get_attribute("href").strip() if website_element else None

                executives = []
                try:
                    page.wait_for_selector("div.table-container table", timeout=7000)
                    exec_rows = page.query_selector_all("div.table-container table tbody tr")
                    for row in exec_rows:
                        name_el = row.query_selector("td:nth-child(1)")
                        title_el = row.query_selector("td:nth-child(2)")
                        if not name_el or not title_el:
                            continue
                        name = name_el.inner_text().strip()
                        title = title_el.inner_text().strip()
                        if title_allowed(title):
                            executives.append({"name": name, "title": title})
                except Exception:
                    executives = []

                if executives:
                    for exec_data in executives:
                        new_exec = Executive(
                            company_id=company.id,
                            name=exec_data["name"],
                            position=exec_data["title"],
                        )
                        db.add(new_exec)
                else:
                    dummy_exec = Executive(
                        company_id=company.id,
                        name="Missed Exec",
                        position="No valid executives found"
                    )
                    db.add(dummy_exec)

                db.commit()
                results.append({
                    "company_id": company.id,
                    "name": company.name,
                    "profile_link": company.profile_link,
                    "country": country,
                    "sector": sector,
                    "industry": industry,
                    "website": website,
                    "executives": executives,
                    "error": None
                })

            except Exception as e:
                dummy_exec = Executive(
                    company_id=company.id,
                    name="Missed Exec",
                    position=f"Crash: {str(e)}"
                )
                db.add(dummy_exec)
                db.commit()
                results.append({
                    "company_id": company.id,
                    "name": company.name,
                    "profile_link": company.profile_link,
                    "country": None,
                    "sector": None,
                    "industry": None,
                    "website": None,
                    "executives": [],
                    "error": f"Crash: {str(e)}"
                })

            time.sleep(1.5)

        browser.close()

    return results

@router.get("/{scrape_id}", response_model=List[ExecutiveOut])
def get_executives_by_scrape(scrape_id: int, db: Session = Depends(get_db)):
    executives = (
        db.query(Executive)
        .join(Company, Executive.company_id == Company.id)
        .filter(Company.scrape_id == scrape_id)
        .all()
    )
    return executives
