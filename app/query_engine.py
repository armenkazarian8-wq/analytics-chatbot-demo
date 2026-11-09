"""Answer analytics questions with SQL over customer-scoped data + retrieval.

CRITICAL: every database query filters by customer_id. Never load another
tenant's posts into the answer path.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.embeddings import cosine_similarity, embed_text
from app.models import Post, PostEmbedding


@dataclass
class QueryResult:
    kind: str
    summary: str
    rows: list[dict[str, Any]]
    meta: dict[str, Any]


def _engagement_expr():
    return Post.likes + Post.comments + Post.shares


def _customer_posts(customer_id: str) -> Select:
    """Base select that ALWAYS scopes to one customer."""
    return select(Post).where(Post.customer_id == customer_id)


def _parse_days(message: str, default: int = 30) -> int:
    m = re.search(r"last\s+(\d+)\s+days?", message, re.I)
    if m:
        return max(1, int(m.group(1)))
    if re.search(r"last\s+week", message, re.I):
        return 7
    if re.search(r"last\s+month|past\s+month", message, re.I):
        return 30
    if re.search(r"last\s+quarter|past\s+90", message, re.I):
        return 90
    return default


def classify_intent(message: str) -> str:
    text = message.lower()
    if any(
        phrase in text
        for phrase in (
            "top post",
            "best post",
            "most engagement",
            "drove the most",
            "highest engagement",
            "which posts",
            "which post",
        )
    ):
        return "top_engagement"
    if any(
        phrase in text
        for phrase in ("total engagement", "sum of", "overall engagement", "totals")
    ):
        return "totals"
    if any(phrase in text for phrase in ("by platform", "platform breakdown", "per platform")):
        return "by_platform"
    if any(phrase in text for phrase in ("most likes", "highest likes", "top liked")):
        return "top_likes"
    if any(phrase in text for phrase in ("most reach", "highest reach", "widest reach")):
        return "top_reach"
    return "retrieval"


def top_engagement(
    session: Session, customer_id: str, *, days: int = 30, limit: int = 5
) -> QueryResult:
    since = date.today() - timedelta(days=days)
    stmt = (
        _customer_posts(customer_id)
        .where(Post.posted_on >= since)
        .order_by(_engagement_expr().desc())
        .limit(limit)
    )
    posts = list(session.scalars(stmt))
    rows = [
        {
            "external_id": p.external_id,
            "platform": p.platform,
            "caption": p.caption,
            "posted_on": p.posted_on.isoformat(),
            "likes": p.likes,
            "comments": p.comments,
            "shares": p.shares,
            "reach": p.reach,
            "engagement": p.engagement,
        }
        for p in posts
    ]
    if not rows:
        summary = f"No posts found for this customer in the last {days} days."
    else:
        top = rows[0]
        summary = (
            f"Top engagement in the last {days} days: "
            f"'{top['caption']}' on {top['platform']} "
            f"({top['engagement']} engagement: {top['likes']} likes, "
            f"{top['comments']} comments, {top['shares']} shares)."
        )
        if len(rows) > 1:
            others = ", ".join(f"#{i+2} '{r['caption']}' ({r['engagement']})" for i, r in enumerate(rows[1:3]))
            summary += f" Next: {others}."
    return QueryResult(
        kind="top_engagement",
        summary=summary,
        rows=rows,
        meta={"customer_id": customer_id, "days": days, "since": since.isoformat()},
    )


def totals(session: Session, customer_id: str, *, days: int = 30) -> QueryResult:
    since = date.today() - timedelta(days=days)
    stmt = select(
        func.count(Post.id),
        func.coalesce(func.sum(Post.likes), 0),
        func.coalesce(func.sum(Post.comments), 0),
        func.coalesce(func.sum(Post.shares), 0),
        func.coalesce(func.sum(Post.reach), 0),
    ).where(Post.customer_id == customer_id, Post.posted_on >= since)
    count, likes, comments, shares, reach = session.execute(stmt).one()
    engagement = int(likes) + int(comments) + int(shares)
    row = {
        "post_count": int(count),
        "likes": int(likes),
        "comments": int(comments),
        "shares": int(shares),
        "reach": int(reach),
        "engagement": engagement,
    }
    summary = (
        f"In the last {days} days this customer published {row['post_count']} posts "
        f"with {row['engagement']} total engagement "
        f"({row['likes']} likes, {row['comments']} comments, {row['shares']} shares) "
        f"and {row['reach']} combined reach."
    )
    return QueryResult(
        kind="totals",
        summary=summary,
        rows=[row],
        meta={"customer_id": customer_id, "days": days, "since": since.isoformat()},
    )


def by_platform(session: Session, customer_id: str, *, days: int = 30) -> QueryResult:
    since = date.today() - timedelta(days=days)
    stmt = (
        select(
            Post.platform,
            func.count(Post.id),
            func.coalesce(func.sum(Post.likes + Post.comments + Post.shares), 0),
        )
        .where(Post.customer_id == customer_id, Post.posted_on >= since)
        .group_by(Post.platform)
        .order_by(func.sum(Post.likes + Post.comments + Post.shares).desc())
    )
    rows = [
        {"platform": platform, "posts": int(count), "engagement": int(eng)}
        for platform, count, eng in session.execute(stmt)
    ]
    if not rows:
        summary = f"No platform data for the last {days} days."
    else:
        parts = [f"{r['platform']}: {r['engagement']} engagement across {r['posts']} posts" for r in rows]
        summary = f"Platform breakdown (last {days} days): " + "; ".join(parts) + "."
    return QueryResult(
        kind="by_platform",
        summary=summary,
        rows=rows,
        meta={"customer_id": customer_id, "days": days},
    )


def top_metric(
    session: Session, customer_id: str, metric: str, *, days: int = 30, limit: int = 5
) -> QueryResult:
    since = date.today() - timedelta(days=days)
    column = {"likes": Post.likes, "reach": Post.reach}[metric]
    stmt = (
        _customer_posts(customer_id)
        .where(Post.posted_on >= since)
        .order_by(column.desc())
        .limit(limit)
    )
    posts = list(session.scalars(stmt))
    rows = [
        {
            "external_id": p.external_id,
            "platform": p.platform,
            "caption": p.caption,
            "posted_on": p.posted_on.isoformat(),
            "likes": p.likes,
            "reach": p.reach,
            "engagement": p.engagement,
        }
        for p in posts
    ]
    if not rows:
        summary = f"No posts found for the last {days} days."
    else:
        top = rows[0]
        summary = (
            f"Highest {metric} in the last {days} days: "
            f"'{top['caption']}' on {top['platform']} "
            f"({metric}={top[metric]}, engagement={top['engagement']})."
        )
    return QueryResult(
        kind=f"top_{metric}",
        summary=summary,
        rows=rows,
        meta={"customer_id": customer_id, "days": days, "metric": metric},
    )


def retrieve_similar(
    session: Session, customer_id: str, message: str, *, limit: int = 5
) -> QueryResult:
    """Vector retrieval over THIS customer's embeddings only."""
    query_vec = embed_text(message)
    stmt = (
        select(PostEmbedding, Post)
        .join(Post, Post.id == PostEmbedding.post_id)
        .where(PostEmbedding.customer_id == customer_id, Post.customer_id == customer_id)
    )
    scored: list[tuple[float, Post]] = []
    for emb, post in session.execute(stmt):
        vec = json.loads(emb.vector_json)
        score = cosine_similarity(query_vec, vec)
        scored.append((score, post))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:limit]
    rows = [
        {
            "external_id": p.external_id,
            "platform": p.platform,
            "caption": p.caption,
            "posted_on": p.posted_on.isoformat(),
            "engagement": p.engagement,
            "similarity": round(score, 4),
        }
        for score, p in top
    ]
    if not rows:
        summary = "No matching posts found for this customer."
    else:
        bits = [
            f"'{r['caption']}' ({r['platform']}, engagement={r['engagement']}, sim={r['similarity']})"
            for r in rows[:3]
        ]
        summary = "Closest posts for this customer: " + "; ".join(bits) + "."
    return QueryResult(
        kind="retrieval",
        summary=summary,
        rows=rows,
        meta={"customer_id": customer_id, "limit": limit},
    )


def run_query(session: Session, customer_id: str, message: str) -> QueryResult:
    """Route the user message to a scoped analytics query."""
    days = _parse_days(message)
    intent = classify_intent(message)
    if intent == "top_engagement":
        return top_engagement(session, customer_id, days=days)
    if intent == "totals":
        return totals(session, customer_id, days=days)
    if intent == "by_platform":
        return by_platform(session, customer_id, days=days)
    if intent == "top_likes":
        return top_metric(session, customer_id, "likes", days=days)
    if intent == "top_reach":
        return top_metric(session, customer_id, "reach", days=days)
    return retrieve_similar(session, customer_id, message)
