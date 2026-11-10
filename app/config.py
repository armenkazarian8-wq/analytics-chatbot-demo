"""Runtime configuration. Defaults favor a zero-dependency local demo."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DEFAULT_SQLITE = DATA_DIR / "analytics.db"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE}")
USE_PGVECTOR = os.getenv("USE_PGVECTOR", "0").lower() in {"1", "true", "yes"}

# Prefer Gemini when GEMINI_API_KEY is set; otherwise OpenAI.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or None
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY") or None

if GEMINI_API_KEY:
    LLM_PROVIDER = "gemini"
    LLM_MODEL = os.getenv("LLM_MODEL") or os.getenv("GEMINI_MODEL") or "gemini-3.5-flash-lite"
elif OPENAI_API_KEY:
    LLM_PROVIDER = "openai"
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
else:
    LLM_PROVIDER = None
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

USE_LLM = LLM_PROVIDER is not None

EMBEDDING_DIM = 64  # small deterministic vectors for local demo

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
