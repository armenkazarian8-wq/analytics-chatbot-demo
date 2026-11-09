"""Chat orchestration: memory + scoped query + optional LLM answer."""

from __future__ import annotations

import json
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.config import LLM_MODEL, OPENAI_API_KEY, USE_LLM
from app.memory import append_message, get_history
from app.models import Customer
from app.query_engine import QueryResult, run_query


def _compose_fallback(
    customer: Customer, message: str, result: QueryResult, history: list[Any]
) -> str:
    prior = ""
    if history:
        last_user = next((m.content for m in reversed(history) if m.role == "user"), None)
        if last_user and last_user != message:
            prior = f" (continuing from earlier: “{last_user[:80]}”)"
    header = (
        f"Answer for {customer.name} only{prior}. "
        f"Query type: {result.kind}."
    )
    return f"{header}\n\n{result.summary}\n\n(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)"


def _compose_with_llm(
    customer: Customer, message: str, result: QueryResult, history: list[Any]
) -> str:
    """Optional OpenAI chat completion. Falls back if the call fails."""
    assert OPENAI_API_KEY
    history_blob = [
        {"role": m.role, "content": m.content}
        for m in history[-6:]
        if m.role in {"user", "assistant"}
    ]
    system = (
        "You are an analytics assistant inside a multi-tenant social media app. "
        f"You may ONLY use data for customer_id={customer.id} ({customer.name}). "
        "Never invent posts or metrics. If the structured result is empty, say so. "
        "Keep answers under 120 words. Mention that figures come from this customer's data."
    )
    user_payload = {
        "question": message,
        "structured_result": {
            "kind": result.kind,
            "summary": result.summary,
            "rows": result.rows[:8],
            "meta": result.meta,
        },
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system},
            *history_blob,
            {"role": "user", "content": json.dumps(user_payload)},
        ],
        "temperature": 0.2,
    }
    try:
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:  # noqa: BLE001 — demo should never crash on LLM
        return (
            _compose_fallback(customer, message, result, history)
            + f"\n\n(LLM unavailable: {type(exc).__name__}; used fallback.)"
        )


def handle_chat(
    session: Session, *, customer_id: str, session_id: str, message: str
) -> dict[str, Any]:
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise ValueError(f"Unknown customer_id: {customer_id}")

    history = get_history(session, customer_id=customer_id, session_id=session_id)
    append_message(
        session, customer_id=customer_id, session_id=session_id, role="user", content=message
    )

    result = run_query(session, customer_id, message)

    # Defense in depth: every returned row must belong to this customer when
    # the row carries a customer_id field (meta always does).
    if result.meta.get("customer_id") != customer_id:
        raise RuntimeError("Isolation violation: query meta customer_id mismatch")

    if USE_LLM:
        answer = _compose_with_llm(customer, message, result, history)
        mode = "llm"
    else:
        answer = _compose_fallback(customer, message, result, history)
        mode = "fallback"

    append_message(
        session, customer_id=customer_id, session_id=session_id, role="assistant", content=answer
    )
    session.commit()

    return {
        "customer_id": customer_id,
        "session_id": session_id,
        "answer": answer,
        "mode": mode,
        "query_kind": result.kind,
        "rows": result.rows,
        "meta": result.meta,
    }
