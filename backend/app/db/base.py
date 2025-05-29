# app/db/base.py
from app.db.session import engine

from app.db.base_class import Base

# ✅ Import all models here so Alembic sees them through Base.metadata
from app.models.user import User
from app.models.scrape import Scrape
from app.models.screener_config import ScreenerConfig
from app.models.company import Company


Base.metadata.create_all(bind=engine)
