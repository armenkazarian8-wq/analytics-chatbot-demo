"""FastAPI entrypoint: /chat API + minimal demo UI."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.chat import handle_chat
from app.config import USE_LLM
from app.db import Base, SessionLocal, engine
from app.models import Customer
from app.seed import seed

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        count = session.scalar(select(func.count()).select_from(Customer)) or 0
        if count == 0:
            seed(session)
    yield


app = FastAPI(
    title="Analytics Chatbot Demo",
    description=(
        "Illustrative multi-tenant analytics chatbot with per-customer isolation. "
        "Uses fictional demo data only. Not a production client deliverable."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatRequest(BaseModel):
    customer_id: str = Field(..., examples=["cust_aurora"])
    session_id: str = Field(..., examples=["demo-session-1"])
    message: str = Field(..., min_length=1, examples=["Which posts drove the most engagement last month?"])


class ChatResponse(BaseModel):
    customer_id: str
    session_id: str
    answer: str
    mode: str
    query_kind: str
    rows: list
    meta: dict


@app.get("/health")
def health():
    return {"ok": True, "llm_enabled": USE_LLM}


@app.get("/customers")
def list_customers(db: Session = Depends(get_db)):
    customers = list(db.scalars(select(Customer).order_by(Customer.id)))
    return [
        {"id": c.id, "name": c.name, "industry": c.industry, "note": "FICTIONAL demo tenant"}
        for c in customers
    ]


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, db: Session = Depends(get_db)):
    try:
        result = handle_chat(
            db,
            customer_id=body.customer_id,
            session_id=body.session_id,
            message=body.message,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
