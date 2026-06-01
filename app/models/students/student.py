from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.core.config import settings
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.projects.project import ProjectModel
    from app.models.projects.project_member import ProjectMemberModel
    from app.models.students.busy_slot import BusySlotModel


class Role(str, Enum):
    ADMIN = settings.role.admin_role_code
    USER = settings.role.default_user_role_code


class StudentBase(SQLModel):
    email: str = Field(index=True, nullable=False, max_length=255)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    hashed_password: str = Field(nullable=False)
    skills: str | None = Field(default=None, sa_column=Column(Text))
    role: str = Field(default=settings.role.default_user_role_code, nullable=False)
    is_email_verificated: bool = Field(default=False, nullable=False)


class StudentPublic(BaseModel, StudentBase):
    pass


class StudentCreate(StudentBase):
    password: str = Field(min_length=8)


class StudentUpdate(SQLModel):
    email: str | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    skills: str | None = Field(default=None)


class StudentModel(StudentPublic, table=True):
    __tablename__ = 'student'

    memberships: list['ProjectMemberModel'] = Relationship(
        sa_relationship=relationship(
            "ProjectMemberModel",
            back_populates='student',
            lazy="selectin",
        )
    )
    owned_projects: list['ProjectModel'] = Relationship(
        sa_relationship=relationship(
            "ProjectModel",
            back_populates="owner",
            lazy="selectin"
        )
    )
    busy_slots: list['BusySlotModel'] = Relationship(
        sa_relationship=relationship(
            "BusySlotModel",
            back_populates='student',
            lazy="selectin",
        )
    )
