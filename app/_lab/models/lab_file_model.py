from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy import Table
from app._core.database import meta_data
from cuid import cuid

lab_files = Table(
    "lab_files",
    meta_data,
    Column("id", String(36), primary_key=True, default=lambda: cuid()),

    Column("lab_id", String(36), ForeignKey("labs.id", ondelete="CASCADE"), nullable=False),
    Column("user_id", String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=False),

    Column("name", String(255), nullable=False),
    Column("path", String(1000), nullable=False),
    Column("content", Text, nullable=False),
    Column("summary", Text, nullable=False),

    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)