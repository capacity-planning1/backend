from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Index
from sqlmodel import Field

from app.models.base import BaseModel


class TokenBlacklistModel(BaseModel, table=True):
    __tablename__ = "token_blacklist"

    jti: str = Field(
        unique=True,
        nullable=False,
        max_length=255
    )
    expires_at: datetime = Field(
        nullable=False,
    )
    student_id: UUID | None = Field(
        default=None,
        nullable=True,
        foreign_key="student.id"
    )

    __table_args__ = (
        Index("ix_token_blacklist_jti", "jti"),
        Index("ix_token_blacklist_expires_at", "expires_at")
    )
