# Analytics Chatbot Demo

**Illustrative demo only.** Built so a freelancer can show an Upwork client what a multi-tenant analytics chatbot looks like. All customers and posts are **fictional** and clearly labeled. This is not a past client project and does not claim any real results.

## What it does

A manager inside a social-media analytics app asks questions like:

> Which posts drove the most engagement last month?

The service answers **only from that manager’s customer data**. Customer A never sees Customer B’s posts.

Stack:

- **Python / FastAPI** — `POST /chat` with `customer_id`, `session_id`, `message`
- **PostgreSQL + pgvector** — intended production path via `docker-compose.yml`
- **SQLite + in-memory-style vectors** — default local path (no Docker required)
- **Minimal chat UI** — single HTML page served by FastAPI (no build step)
- **Optional LLM** — if `OPENAI_API_KEY` is set; otherwise a deterministic fallback composes answers from SQL/retrieval results

## Quick start (local, no Docker)

```bash
cd analytics-chatbot-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000

### Example API call

```bash
curl -s http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": "cust_aurora",
    "session_id": "demo-1",
    "message": "Which posts drove the most engagement last month?"
  }' | python -m json.tool
```

Demo tenants: `cust_aurora`, `cust_nimbus`, `cust_pixelpine`.

## Optional: Postgres + pgvector

```bash
docker compose up -d
export DATABASE_URL=postgresql+psycopg://demo:demo@localhost:5432/analytics_chat
export USE_PGVECTOR=1
pip install 'psycopg[binary]>=3.1'
python -m app.seed
uvicorn app.main:app --reload
```

The portable SQLite path stores embedding vectors as JSON on `post_embeddings`. With Postgres you can replace that column with a native `vector` type; the **isolation rule does not change**: every query filters by `customer_id`.

## Optional: LLM answers

```bash
export OPENAI_API_KEY=sk-...
export LLM_MODEL=gpt-4o-mini   # optional
```

Without a key, answers are built directly from structured query results (deterministic demo mode).

## Architecture

```
Client (HTML UI or API)
        │
        ▼
   FastAPI /chat
        │
        ├─ validate customer_id
        ├─ append user message (scoped by customer_id + session_id)
        ├─ query_engine.run_query(customer_id, message)
        │     • structured intents → SQL on posts WHERE customer_id = ?
        │     • free text → cosine retrieval on THAT customer’s embeddings only
        ├─ compose answer (LLM or fallback)
        └─ append assistant message (same scope)
```

### How isolation works

1. **Every** `SELECT` on posts/embeddings includes `WHERE customer_id = :customer_id`.
2. Embedding retrieval joins posts and filters both `PostEmbedding.customer_id` and `Post.customer_id`.
3. Chat memory is keyed by `(customer_id, session_id)` — the same session string used by two customers does not share history.
4. Response `meta.customer_id` is checked before returning.
5. Pytest (`tests/test_isolation.py`) asserts Customer A answers never contain Customer B captions, and that a query whose global nearest neighbor is on B still returns only A’s posts when asked as A.

## Tests

```bash
pytest -q
```

## Project layout

```
app/
  main.py          FastAPI routes + static UI
  chat.py          orchestration, optional LLM
  query_engine.py  SQL + retrieval (always scoped)
  embeddings.py    deterministic local vectors
  memory.py        per-session history
  models.py        ORM
  seed.py          fictional data
static/index.html  demo chat page
tests/             isolation + chat tests
docker-compose.yml optional pgvector
DEMO.md            sample Q&A transcript
```

## Honesty note

This repository was built as a **portfolio / proposal sample** with generated fake data. Do not present it as work delivered for a named client.
