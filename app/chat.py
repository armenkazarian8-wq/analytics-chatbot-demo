"""Chat orchestration: memory + scoped query + optional LLM answer."""

from __future__ import annotations

import json
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.config import (
    GEMINI_API_KEY,
    LLM_MODEL,
    LLM_PROVIDER,
    OPENAI_API_KEY,
    USE_LLM,
)
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
    return (
        f"{header}\n\n{result.summary}\n\n"
        "(Demo mode: deterministic answer from this customer's data. "
        "No other tenants were queried.)"
    )


def _system_prompt(customer: Customer) -> str:
    return (
        "You are an analytics assistant inside a multi-tenant social media app. "
        f"You may ONLY use data for customer_id={customer.id} ({customer.name}). "
        "Never invent posts or metrics. Base every claim on the structured_result "
        "JSON only — that payload already contains only this customer's rows. "
        "If the structured result is empty, say so. "
        "Keep answers under 120 words. Mention that figures come from this customer's data."
    )


def _user_payload(message: str, result: QueryResult) -> dict[str, Any]:
    return {
        "question": message,
        "structured_result": {
            "kind": result.kind,
            "summary": result.summary,
            "rows": result.rows[:8],
            "meta": result.meta,
        },
    }


def _compose_with_openai(
    customer: Customer, message: str, result: QueryResult, history: list[Any]
) -> str:
    assert OPENAI_API_KEY
    history_blob = [
        {"role": m.role, "content": m.content}
        for m in history[-6:]
        if m.role in {"user", "assistant"}
    ]
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": _system_prompt(customer)},
            *history_blob,
            {"role": "user", "content": json.dumps(_user_payload(message, result))},
        ],
        "temperature": 0.2,
    }
    resp = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json=payload,
        timeout=45.0,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def _compose_with_gemini(
    customer: Customer, message: str, result: QueryResult, history: list[Any]
) -> str:
    """Google Gemini generateContent. Key is sent via header only, never logged."""
    assert GEMINI_API_KEY
    contents: list[dict[str, Any]] = []
    for m in history[-6:]:
        if m.role == "user":
            contents.append({"role": "user", "parts": [{"text": m.content}]})
        elif m.role == "assistant":
            contents.append({"role": "model", "parts": [{"text": m.content}]})
    contents.append(
        {
            "role": "user",
            "parts": [{"text": json.dumps(_user_payload(message, result))}],
        }
    )
    payload = {
        "system_instruction": {"parts": [{"text": _system_prompt(customer)}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1024,
        },
    }
    # Header auth keeps the key out of request URLs that might appear in traces.
    resp = httpx.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{LLM_MODEL}:generateContent",
        headers={
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60.0,
    )
    resp.raise_for_status()
    data = resp.json()
    parts = data["candidates"][0]["content"]["parts"]
    texts = [p.get("text", "") for p in parts if p.get("text")]
    answer = "\n".join(texts).strip()
    if not answer:
        raise RuntimeError("Gemini returned empty text")
    return answer


def _compose_with_llm(
    customer: Customer, message: str, result: QueryResult, history: list[Any]
) -> str:
    """Optional LLM phrasing over tenant-scoped structured results. Falls back on error."""
    try:
        if LLM_PROVIDER == "gemini":
            return _compose_with_gemini(customer, message, result, history)
        if LLM_PROVIDER == "openai":
            return _compose_with_openai(customer, message, result, history)
        raise RuntimeError(f"Unknown LLM provider: {LLM_PROVIDER}")
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
        "provider": LLM_PROVIDER if mode == "llm" else None,
        "query_kind": result.kind,
        "rows": result.rows,
        "meta": result.meta,
    }
