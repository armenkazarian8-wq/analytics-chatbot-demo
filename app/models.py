"""ORM models for customers, posts, embeddings, and chat memory."""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    industry: Mapped[str] = mapped_column(String(64), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="customer")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("customer_id", "external_id", name="uq_post_ext"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("customers.id"), nullable=False, index=True
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False)
    platform: Mapped[str] = mapped_column(String(32), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=False)
    posted_on: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    comments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shares: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reach: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    customer: Mapped[Customer] = relationship(back_populates="posts")

    @property
    def engagement(self) -> int:
        return int(self.likes) + int(self.comments) + int(self.shares)


class PostEmbedding(Base):
    """Stores a JSON-serialized vector for local/SQLite mode.

    With USE_PGVECTOR=1 you would store a native vector column instead;
    this table keeps the demo portable without Docker.
    """

    __tablename__ = "post_embeddings"

    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), primary_key=True
    )
    customer_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("customers.id"), nullable=False, index=True
    )
    vector_json: Mapped[str] = mapped_column(Text, nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("customers.id"), nullable=False, index=True
    )
    session_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(16), nullable=False)  # user | assistant
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
