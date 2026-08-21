from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Item


app = FastAPI(title="Home Lab API", version="0.1.0")


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemResponse(ItemCreate):
    id: int

    model_config = {"from_attributes": True}


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "ok"}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "not_ready", "database": str(exc)},
        ) from exc


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = Item(name=payload.name, description=payload.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items", response_model=list[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).order_by(Item.id).all()
