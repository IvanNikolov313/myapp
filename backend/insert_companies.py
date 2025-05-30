import csv
from app.db.session import SessionLocal
from app.models.company import Company

def run():
    db = SessionLocal()
    with open("data/usa_master_csv.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = Company(
                name=row["name"],
                symbol=row["symbol"],
                profile_link=row["profile_link"],
                market_cap=row.get("market_cap") or None,
                sector=row.get("sector") or None,
                industry=row.get("industry") or None,
                website=row.get("website") or None,
                country=row.get("country") or None,
                scrape_id=None  # Master import = null
            )
            db.add(company)

        db.commit()
        db.close()

if __name__ == "__main__":
    run()
