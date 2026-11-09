"""Prove customer A can never see customer B's data."""

from __future__ import annotations

import json

from sqlalchemy import select

from app.chat import handle_chat
from app.embeddings import cosine_similarity, embed_text
from app.models import Post, PostEmbedding
from app.query_engine import retrieve_similar, run_query, top_engagement


CUSTOMER_A = "cust_aurora"
CUSTOMER_B = "cust_nimbus"
CUSTOMER_C = "cust_pixelpine"


def test_posts_are_partitioned_by_customer(db):
    a_ids = {p.external_id for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_A))}
    b_ids = {p.external_id for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_B))}
    assert a_ids
    assert b_ids
    # Same external_id labels are OK across tenants; row identity is customer-scoped.
    a_captions = {
        p.caption for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_A))
    }
    b_captions = {
        p.caption for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_B))
    }
    assert a_captions.isdisjoint(b_captions)


def test_top_engagement_never_leaks_other_customer(db):
    result = top_engagement(db, CUSTOMER_A, days=90, limit=20)
    assert result.meta["customer_id"] == CUSTOMER_A
    b_captions = {
        p.caption for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_B))
    }
    c_captions = {
        p.caption for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_C))
    }
    for row in result.rows:
        assert row["caption"] not in b_captions
        assert row["caption"] not in c_captions
        # Every returned caption must belong to A.
        assert (
            db.scalar(
                select(Post).where(
                    Post.customer_id == CUSTOMER_A, Post.caption == row["caption"]
                )
            )
            is not None
        )


def test_retrieval_only_searches_requesting_customer(db):
    # Ask something that would strongly match B's famous latte-art post if leaked.
    result = retrieve_similar(db, CUSTOMER_A, "latte art coffee roasting beans", limit=10)
    assert result.meta["customer_id"] == CUSTOMER_A
    leaked = [r for r in result.rows if "latte" in r["caption"].lower() or "coffee" in r["caption"].lower() and "trail" not in r["caption"].lower()]
    # Aurora is outdoor gear — should not surface Nimbus coffee posts.
    b_captions = {
        p.caption for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_B))
    }
    for row in result.rows:
        assert row["caption"] not in b_captions
    assert leaked == [] or all(r["caption"] not in b_captions for r in result.rows)


def test_embeddings_table_is_customer_scoped(db):
    emb_rows = list(db.scalars(select(PostEmbedding).where(PostEmbedding.customer_id == CUSTOMER_A)))
    assert emb_rows
    for emb in emb_rows:
        post = db.get(Post, emb.post_id)
        assert post is not None
        assert post.customer_id == CUSTOMER_A
        assert emb.customer_id == CUSTOMER_A


def test_chat_answer_for_a_excludes_b_captions(db):
    out = handle_chat(
        db,
        customer_id=CUSTOMER_A,
        session_id="iso-test",
        message="Which posts drove the most engagement last month?",
    )
    b_captions = {
        p.caption for p in db.scalars(select(Post).where(Post.customer_id == CUSTOMER_B))
    }
    for caption in b_captions:
        assert caption not in out["answer"]
    assert out["meta"]["customer_id"] == CUSTOMER_A


def test_cross_customer_session_ids_do_not_share_memory(db):
    handle_chat(
        db,
        customer_id=CUSTOMER_A,
        session_id="shared-looking-id",
        message="Which posts drove the most engagement last month?",
    )
    out_b = handle_chat(
        db,
        customer_id=CUSTOMER_B,
        session_id="shared-looking-id",
        message="What are total engagement totals last month?",
    )
    # B's answer must reference B's data path only.
    assert out_b["meta"]["customer_id"] == CUSTOMER_B
    a_unique = "trail pack"  # aurora-only phrase
    # Totals answer may not mention captions; ensure aurora-specific caption never appears.
    assert a_unique.lower() not in out_b["answer"].lower()


def test_vector_index_cannot_rank_foreign_posts_into_a(db):
    """Even if we manually compute similarities against all posts, the engine filters."""
    query = embed_text("Latte art fail compilation cold brew")
    all_emb = list(db.execute(select(PostEmbedding, Post).join(Post, Post.id == PostEmbedding.post_id)))
    best_overall = max(
        all_emb, key=lambda pair: cosine_similarity(query, json.loads(pair[0].vector_json))
    )
    # Best overall should be a Nimbus post, but retrieve_similar for A must not return it.
    assert best_overall[1].customer_id == CUSTOMER_B
    scoped = retrieve_similar(db, CUSTOMER_A, "Latte art fail compilation cold brew", limit=5)
    for row in scoped.rows:
        post = db.scalar(select(Post).where(Post.caption == row["caption"]))
        assert post.customer_id == CUSTOMER_A
