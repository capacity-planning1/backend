from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.student import StudentModel
    from app.models.task_assignment import TaskAssignmentModel


class SlotType(str, Enum):
    PAIR = 'pair'
    CREDIT = 'credit'
    EXAM = 'exam'
    PERSONAL = 'personal'


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
