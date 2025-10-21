from sqlalchemy import (
    Table, Column, String, ForeignKey,
    DateTime, Text, func
)
from sqlalchemy.dialects.postgresql import ENUM
from cuid import cuid
from app._core.database import meta_data

role_enum = ENUM("user", "assistant", "system", name="role", metadata=meta_data)


lab_chat_sessions = Table(
    "lab_chat_sessions",
    meta_data,
    Column("id", String(36), primary_key=True, default=lambda: cuid()),
    Column(
        "lab_id",
        String(36),
        ForeignKey("labs.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)


lab_chat_messages = Table(
    "lab_chat_messages",
    meta_data,
    Column("id", String(36), primary_key=True, default=lambda: cuid()),
    Column(
        "session_id",
        String(36),
        ForeignKey("lab_chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "user_id",
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("role", role_enum, nullable=False),
    Column("content", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
