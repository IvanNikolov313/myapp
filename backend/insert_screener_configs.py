# insert_screener_configs.py

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.models import screener_config as screener_model
from app.db.base import Base

DATABASE_URL = "postgresql://appuser:password@myapp-db:5432/appdb"
engine = create_engine(DATABASE_URL)

db = Session(bind=engine)

configs = [
    {"region": "USA", "market_cap": "$50M–$2B", "label": "us_smallcap"},
    {"region": "Canada", "market_cap": "$10M–$1B", "label": "ca_microcap"},
]

for cfg in configs:
    config = screener_model.ScreenerConfig(**cfg)
    db.add(config)

db.commit()
db.close()

print("✅ Seeded screener_configs into database.")
