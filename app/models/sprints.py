from datetime import date, datetime, timezone
from enum import Enum
from uuid import UUID

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class StatusType(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    REVIEW = 'review'
    TESTING = 'testing'
    DONE = 'done'


class TaskPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskChangeRequestStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class Sprint(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    project_id: UUID = Field(foreign_key='project.id', nullable=False)

    name: str = Field(nullable=False, max_length=100)

    start_date: date = Field(nullable=False)

    end_date: date = Field(nullable=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SprintTask(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    project_id: UUID = Field(foreign_key='project.id', nullable=False)

    sprint_id: int = Field(foreign_key='sripnt.id', nullable=False)

    title: str = Field(nullable=False, max_length=255)

    description: str | None = Field(default=None, sa_column=Column(Text))

    status: StatusType = Field(default=StatusType.OPEN)

    priority: TaskPriority = Field(default=TaskPriority.LOW)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskAssignment(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    project_task_id: UUID = Field(foreign_key='projecttask.id', nullable=False)

    project_member_id: UUID = Field(foreign_key='projectmember.id', nullable=False)

    assignet_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    accepted_at: datetime | None = Field(default=None)


class TaskChangeRequest(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    task_assignment_id: UUID = Field(foreign_key='taskassignment.id', nullable=False)

    requested_by_member_id: UUID = Field(foreign_key='projectmember.id', nullable=False)

    reason: str | None = Field(default=None, sa_column=Column(Text))

    status: TaskChangeRequestStatus = Field(default=TaskChangeRequestStatus.PENDING)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    handled_at: datetime | None = Field(default=None)
