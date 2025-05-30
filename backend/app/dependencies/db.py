from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    print("Connected to DB:", db.bind.url)  # Add this line to verify DB connection
    try:
        yield db
    finally:
        db.close()
