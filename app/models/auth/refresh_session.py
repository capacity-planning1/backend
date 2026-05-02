from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Index, SQLModel

from app.models.base import BaseModel


class RefreshSessionModel(BaseModel, table=True):
    __tablename__ = "refresh_session"

    jti: str = Field(
        unique=True,
        nullable=False,
        max_length=255
    )
    student_id: UUID = Field(
        nullable=False,
        foreign_key="student.id",
        index=True
    )
    expires_at: datetime = Field(
        nullable=False,
    )
    is_revoked: bool = Field(
        default=False,
        nullable=False
    )
    user_agent: str | None = Field(default=None, nullable=True)
    ip_address: str | None = Field(default=None, nullable=True)

    __table_args__ = (
        Index("ix_refresh_session_jti", "jti"),
        Index("ix_refresh_session_student_id", "student_id"),
        Index("ix_refresh_session_expires_at", "expires_at")
    )

class RefreshSessionCreate(RefreshSessionModel):
    pass


class RefreshSessionUpdate(SQLModel):
    jti: str | None = None
    expires_at: datetime | None = None
    is_revoked: bool | None = None

