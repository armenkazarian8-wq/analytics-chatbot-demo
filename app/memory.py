"""Per-session conversation memory, always scoped by customer_id."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ChatMessage


def append_message(
    session: Session, *, customer_id: str, session_id: str, role: str, content: str
) -> ChatMessage:
    msg = ChatMessage(
        customer_id=customer_id,
        session_id=session_id,
        role=role,
        content=content,
    )
    session.add(msg)
    session.flush()
    return msg


def get_history(
    session: Session, *, customer_id: str, session_id: str, limit: int = 12
) -> list[ChatMessage]:
    """Return recent messages for this customer+session only."""
    stmt = (
        select(ChatMessage)
        .where(
            ChatMessage.customer_id == customer_id,
            ChatMessage.session_id == session_id,
        )
        .order_by(ChatMessage.id.asc())
        .limit(limit)
    )
    return list(session.scalars(stmt))
