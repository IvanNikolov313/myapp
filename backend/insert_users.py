from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.models import user as user_model
from app.db.base import Base
from app.core.security import get_password_hash  # your passlib hashing function

DATABASE_URL = "postgresql://appuser:password@myapp-db:5432/appdb"
engine = create_engine(DATABASE_URL)

db = Session(bind=engine)

users = [
    {"email": "admin@example.com", "password": "adminpass"},
    {"email": "test@example.com", "password": "testpass"},
]

for u in users:
    hashed = get_password_hash(u["password"])  # Passlib hash
    user = user_model.User(email=u["email"], hashed_password=hashed, is_active=True)
    db.add(user)

db.commit()
db.close()

print("✅ Seeded users into database.")
