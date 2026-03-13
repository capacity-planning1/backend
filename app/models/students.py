from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    email: str = Field(index=True, nullable=False, max_length=255)

    first_name: str = Field(nullable=False, max_length=100)

    last_name: str = Field(nullable=False, max_length=100)

    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    skills: str | None = Field(default=None, sa_column=Column(Text))
