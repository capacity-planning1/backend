from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """Base mixin with UUID PK and audit timestamps."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        sa_type=TIMESTAMP(timezone=True),
    )
