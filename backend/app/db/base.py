# app/db/base.py
from app.db.session import engine

from app.db.base_class import Base

import app.models

Base.metadata.create_all(bind=engine)
