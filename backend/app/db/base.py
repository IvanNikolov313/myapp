# app/db/base.py
from app.db.session import engine

from .base_class import Base
from app.models import screener_config
from app.models import scrape  # ← just importing triggers table creation
from app.models.user import User


Base.metadata.create_all(bind=engine)
