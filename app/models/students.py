from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class SlotType(str, Enum):
    PAIR = 'pair'
    CREDIT = 'credit'
    EXAM = 'exam'
    PERSONAL = 'personal'


class Student(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    email: str = Field(index=True, nullable=False, max_length=255)

    first_name: str = Field(nullable=False, max_length=100)

    last_name: str = Field(nullable=False, max_length=100)

    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    skills: str | None = Field(default=None, sa_column=Column(Text))


class BusySlot(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    student_id: UUID = Field(foreign_key='student.id')

    slot_type: SlotType = Field(nullable=False)

    start_datetime: datetime = Field(nullable=False)

    end_datetime: datetime = Field(nullable=False)

    title: str = Field(nullable=False, max_length=255)

    description: str | None = Field(default=None, sa_column=Column(Text))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    source: str = Field(nullable=False, max_length=50)

    task_assignment_id: UUID = Field(foreign_key='taskassignment.id', nullable=False)
