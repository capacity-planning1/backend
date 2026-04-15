from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Column, Text, TIMESTAMP
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


class BusySlotBase(SQLModel):
    student_id: UUID = Field(foreign_key='student.id', nullable=False)
    slot_type: SlotType = Field(nullable=False)
    start_datetime: datetime = Field(nullable=False)
    end_datetime: datetime = Field(nullable=False)
    description: str | None = Field(default=None, sa_column=Column(Text))
    task_assignment_id: UUID = Field(foreign_key="taskassignment.id", nullable=False)


class BusySlotPublic(BaseModel, BusySlotBase):
    pass


class BusySlotCreate(BusySlotBase):
    pass


class BusySlotUpdate(SQLModel):
    slot_type: SlotType | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    description: str | None = None


class BusySlotModel(BusySlotPublic, table=True):
    __tablename__ = 'busyslot'

    student: StudentModel = Relationship(
        back_populates="busy_slots",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    task_assignment: TaskAssignmentModel = Relationship(
        back_populates="busy_slots",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
