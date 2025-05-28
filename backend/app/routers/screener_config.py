from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError

from app.dependencies.db import get_db
from app.core.security import verify_token
from app.models.screener_config import ScreenerConfig
from app.schemas.screener_config import ScreenerConfigCreate, ScreenerConfigOut

router = APIRouter(tags=["Screener Configs"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/screener-configs", response_model=List[ScreenerConfigOut])
def get_all(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        print("✅ Token verified for:", payload)
        results = db.query(ScreenerConfig).all()
        print("✅ Returned configs:", results)
        return results
    except JWTError as e:
        print("❌ JWT error:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        print("❌ Unexpected error in get_all:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/screener-configs", response_model=ScreenerConfigOut)
def create(config: ScreenerConfigCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        verify_token(token)
        obj = ScreenerConfig(**config.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except JWTError as e:
        print("❌ JWT error:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        print("❌ Unexpected error in create:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/screener-configs/{id}", response_model=ScreenerConfigOut)
def update(id: int, config: ScreenerConfigCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        verify_token(token)
        obj = db.query(ScreenerConfig).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        for key, value in config.dict().items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj
    except JWTError as e:
        print("❌ JWT error:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        print("❌ Unexpected error in update:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/screener-configs/{id}")
def delete(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        verify_token(token)
        obj = db.query(ScreenerConfig).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(obj)
        db.commit()
        return {"message": "Deleted"}
    except JWTError as e:
        print("❌ JWT error:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        print("❌ Unexpected error in delete:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
