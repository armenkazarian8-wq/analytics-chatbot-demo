"""Shared fixtures: fresh seeded SQLite DB per test session."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Point at a temp SQLite file before app imports bind the engine.
TEST_DB = Path("/tmp/analytics_chatbot_demo_test.db")
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
# Force deterministic fallback so tests do not call external LLMs.
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("LLM_API_KEY", None)
os.environ.pop("GEMINI_API_KEY", None)

from app.db import Base, SessionLocal, engine  # noqa: E402
from app.seed import seed  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
