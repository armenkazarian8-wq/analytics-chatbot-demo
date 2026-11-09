"""Chat endpoint behavior and structured Q&A."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.chat import handle_chat
from app.main import app
from app.query_engine import classify_intent, run_query


def test_classify_top_engagement():
    assert classify_intent("Which posts drove the most engagement last month?") == "top_engagement"


def test_structured_top_posts(db):
    result = run_query(db, "cust_nimbus", "Which posts drove the most engagement last month?")
    assert result.kind == "top_engagement"
    assert result.rows
    engagements = [r["engagement"] for r in result.rows]
    assert engagements == sorted(engagements, reverse=True)


def test_handle_chat_fallback_mode(db):
    out = handle_chat(
        db,
        customer_id="cust_pixelpine",
        session_id="s1",
        message="Platform breakdown last month",
    )
    assert out["mode"] == "fallback"
    assert out["query_kind"] == "by_platform"
    assert "Pixel Pine" in out["answer"]


def test_conversation_memory(db):
    handle_chat(
        db,
        customer_id="cust_aurora",
        session_id="mem-1",
        message="Which posts drove the most engagement last month?",
    )
    out2 = handle_chat(
        db,
        customer_id="cust_aurora",
        session_id="mem-1",
        message="What are the totals last month?",
    )
    assert "continuing from earlier" in out2["answer"].lower()


def test_http_chat_endpoint(db):  # db fixture ensures seed
    client = TestClient(app)
    res = client.post(
        "/chat",
        json={
            "customer_id": "cust_aurora",
            "session_id": "http-1",
            "message": "Which posts drove the most engagement last month?",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["customer_id"] == "cust_aurora"
    assert body["rows"]


def test_unknown_customer_404(db):
    client = TestClient(app)
    res = client.post(
        "/chat",
        json={"customer_id": "cust_nope", "session_id": "x", "message": "hi"},
    )
    assert res.status_code == 404
