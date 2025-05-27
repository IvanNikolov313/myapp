from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.models import scrape as scrape_model
from app.db.base import Base  # triggers create_all
from app.db.session import engine

DATABASE_URL = "postgresql://appuser:password@myapp-db:5432/appdb"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

db = Session(bind=engine)

scrape = scrape_model.Scrape(
    config_id=1,
    total_companies=120,
    new_companies=37,
)
db.add(scrape)

db.commit()
db.close()

print("✅ Scrape seeded successfully.")
