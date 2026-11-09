"""Generate clearly labeled fictional analytics data for three demo customers."""

from __future__ import annotations

import json
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.db import Base, SessionLocal, engine
from app.embeddings import embed_text
from app.models import Customer, Post, PostEmbedding

# All names are fictional. This is demo data only.
CUSTOMERS = [
    {
        "id": "cust_aurora",
        "name": "Aurora Trail Co. (FICTIONAL)",
        "industry": "outdoor gear",
        "posts": [
            ("p1", "instagram", "Sunrise hike tips for weekend warriors", 42, 890, 120, 45, 12000),
            ("p2", "instagram", "New trail pack drop — waterproof and light", 35, 2100, 340, 180, 28000),
            ("p3", "tiktok", "Packing a 3-day backpack in 60 seconds", 28, 5400, 620, 900, 95000),
            ("p4", "instagram", "Customer photo: summit coffee ritual", 21, 1500, 210, 95, 22000),
            ("p5", "twitter", "Rainy season gear checklist", 14, 420, 55, 80, 9000),
            ("p6", "instagram", "Behind the scenes: stitching our packs", 10, 680, 90, 40, 11000),
            ("p7", "tiktok", "Wrong way vs right way to lace hiking boots", 7, 3200, 410, 700, 72000),
            ("p8", "instagram", "Fall foliage trail map giveaway", 3, 980, 160, 70, 15000),
        ],
    },
    {
        "id": "cust_nimbus",
        "name": "Nimbus Bean Roasters (FICTIONAL)",
        "industry": "coffee",
        "posts": [
            ("p1", "instagram", "Ethiopian single-origin tasting notes", 40, 1200, 180, 60, 18000),
            ("p2", "tiktok", "Latte art fail compilation (then the fix)", 33, 8900, 1100, 1500, 140000),
            ("p3", "instagram", "Subscription box unboxing", 25, 760, 95, 40, 12000),
            ("p4", "twitter", "Why we roast darker for espresso", 18, 310, 48, 90, 7000),
            ("p5", "instagram", "Meet the farmers — fictional co-op story", 12, 540, 70, 25, 9500),
            ("p6", "tiktok", "Cold brew concentrate how-to", 8, 4100, 520, 880, 88000),
            ("p7", "instagram", "Limited winter blend launch", 5, 1900, 260, 140, 26000),
            ("p8", "instagram", "Cafe playlist for deep work", 2, 430, 40, 15, 8000),
        ],
    },
    {
        "id": "cust_pixelpine",
        "name": "Pixel Pine Studio (FICTIONAL)",
        "industry": "creative agency",
        "posts": [
            ("p1", "instagram", "Brand refresh case study (demo)", 38, 670, 88, 55, 14000),
            ("p2", "linkedin", "How we run weekly creative critiques", 30, 920, 140, 110, 19000),
            ("p3", "instagram", "Motion design process reel", 22, 2400, 310, 220, 41000),
            ("p4", "twitter", "Hiring junior designer — demo post", 15, 280, 35, 40, 6000),
            ("p5", "instagram", "Color systems that scale", 11, 1100, 150, 70, 17000),
            ("p6", "linkedin", "Client kickoff checklist template", 6, 1500, 210, 180, 25000),
            ("p7", "instagram", "Office plant tour (yes, really)", 4, 500, 60, 20, 9000),
            ("p8", "tiktok", "Before/after logo animation", 1, 3600, 440, 650, 78000),
        ],
    },
]


def _posted_on(days_ago: int) -> date:
    return date.today() - timedelta(days=days_ago)


def seed(session: Session | None = None) -> None:
    """Create tables and load fictional customers/posts/embeddings."""
    own_session = session is None
    if own_session:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        session = SessionLocal()

    assert session is not None
    try:
        for cust in CUSTOMERS:
            session.add(
                Customer(id=cust["id"], name=cust["name"], industry=cust["industry"])
            )
            for ext_id, platform, caption, days_ago, likes, comments, shares, reach in cust[
                "posts"
            ]:
                post = Post(
                    customer_id=cust["id"],
                    external_id=ext_id,
                    platform=platform,
                    caption=caption,
                    posted_on=_posted_on(days_ago),
                    likes=likes,
                    comments=comments,
                    shares=shares,
                    reach=reach,
                )
                session.add(post)
                session.flush()
                vector = embed_text(
                    f"{platform} {caption} likes={likes} comments={comments} shares={shares}"
                )
                session.add(
                    PostEmbedding(
                        post_id=post.id,
                        customer_id=cust["id"],
                        vector_json=json.dumps(vector),
                    )
                )
        session.commit()
    finally:
        if own_session:
            session.close()


if __name__ == "__main__":
    seed()
    print("Seeded fictional demo data for cust_aurora, cust_nimbus, cust_pixelpine.")
