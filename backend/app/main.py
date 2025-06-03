from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import verify_password, create_access_token, verify_token

# Import existing routers
from app.routers.screener_config import router as screener_config_router
from app.routers import scrapes
from app.routers import executives
# Import your new USA Master Summary router
from app.routers import usa_master_sum  # Adjust if your path differs

app = FastAPI()

# Allowed origins for CORS (frontend running on 5173 or 5174)
origins = [
    "http://localhost:5174",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

@app.get("/")
def root():
    return {"message": "Backend running!"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": f"Hello {payload.get('sub')}"}

# Mount existing routers under /api
app.include_router(screener_config_router, prefix="/api")

app.include_router(scrapes.router, prefix="/api")
app.include_router(executives.router, prefix="/api")

# Mount your new USA master summary router under /api
app.include_router(usa_master_sum.router, prefix="/api")
