from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.projects import ProjectMemberModel, ProjectModel
    from app.models.sprints import TaskAssignmentModel


class SlotType(str, Enum):
    PAIR = 'pair'
    CREDIT = 'credit'
    EXAM = 'exam'
    PERSONAL = 'personal'


class StudentBase(SQLModel):
    email: str = Field(index=True, nullable=False, max_length=255)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    skills: str | None = Field(default=None, sa_column=Column(Text))


class StudentPublic(BaseModel, StudentBase):
    pass


class StudentCreate(StudentBase):
    pass


class StudentUpdate(SQLModel):
    email: str | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    skills: str | None = Field(default=None)


class StudentModel(StudentPublic, table=True):
    __tablename__ = 'student'

    memberships: list['ProjectMemberModel'] = Relationship(
        back_populates='student',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    owned_projects: list['ProjectModel'] = Relationship(
        back_populates='owner',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    busy_slots: list['BusySlotModel'] = Relationship(
        back_populates='student',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )


class BusySlotBase(SQLModel):
    student_id: UUID = Field(foreign_key='student.id', nullable=False)
    slot_type: SlotType = Field(nullable=False)
    start_datetime: datetime = Field(nullable=False)
    end_datetime: datetime = Field(nullable=False)
    title: str = Field(nullable=False, max_length=255)
    description: str | None = Field(default=None, sa_column=Column(Text))
    source: str = Field(nullable=False, max_length=50)
    task_assignment_id: UUID = Field(foreign_key='taskassignment.id', nullable=False)


class BusySlotPublic(BaseModel, BusySlotBase):
    pass


class BusySlotCreate(BusySlotBase):
    pass


class BusySlotUpdate(SQLModel):
    slot_type: SlotType | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    source: str | None = Field(default=None, max_length=50)


class BusySlotModel(BusySlotPublic, table=True):
    __tablename__ = 'busyslot'

    student: 'StudentModel' = Relationship(
        back_populates='busy_slots',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    task_assignment: 'TaskAssignmentModel' = Relationship(
        back_populates='busy_slots',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
