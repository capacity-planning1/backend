from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text, TIMESTAMP
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.project_member import ProjectMemberModel
    from app.models.project import ProjectModel
    from app.models.busy_slot import BusySlotModel


class StudentBase(SQLModel):
    email: str = Field(index=True, nullable=False, max_length=255)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    skills: str | None = Field(default=None, sa_column=Column(Text))


class StudentPublic(BaseModel, StudentBase):
    pass


class StudentCreate(StudentBase):
    password_hash: str = Field(nullable=False, max_length=255)


class StudentUpdate(SQLModel):
    email: str | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    skills: str | None = Field(default=None)
    password_hash: str | None = Field(default=None, max_length=255)


class StudentModel(StudentPublic, table=True):
    __tablename__ = 'student'

    password_hash: str = Field(nullable=False, max_length=255)
    registered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),
    )

    memberships: list[ProjectMemberModel] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    owned_projects: list[ProjectModel] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    busy_slots: list[BusySlotModel] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
