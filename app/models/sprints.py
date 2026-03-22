from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.projects import ProjectMemberModel, ProjectModel
    from app.models.students import BusySlotModel


class StatusType(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    TESTING = "testing"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TaskChangeRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class SprintBase(SQLModel):
    project_id: UUID = Field(foreign_key="project.id", nullable=False)
    name: str = Field(nullable=False, max_length=100)
    start_date: date = Field(nullable=False)
    end_date: date = Field(nullable=False)


class SprintPublic(BaseModel, SprintBase):
    pass


class SprintCreate(SprintBase):
    pass


class SprintUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=100)
    start_date: date | None = None
    end_date: date | None = None


class SprintModel(SprintPublic, table=True):
    __tablename__ = "sprint"

    project: "ProjectModel" = Relationship(
        back_populates="sprints",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    tasks: list["SprintTaskModel"] = Relationship(
        back_populates="sprint",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class SprintTaskBase(SQLModel):
    project_id: UUID = Field(foreign_key="project.id", nullable=False)
    sprint_id: UUID = Field(foreign_key="sprint.id", nullable=False)
    title: str = Field(nullable=False, max_length=255)
    description: str | None = Field(default=None, sa_column=Column(Text))
    status: StatusType = Field(default=StatusType.OPEN, nullable=False)
    priority: TaskPriority = Field(default=TaskPriority.LOW, nullable=False)


class SprintTaskPublic(BaseModel, SprintTaskBase):
    pass


class SprintTaskCreate(SprintTaskBase):
    pass


class SprintTaskUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    status: StatusType | None = None
    priority: TaskPriority | None = None


class SprintTaskModel(SprintTaskPublic, table=True):
    __tablename__ = "sprinttask"

    sprint: "SprintModel" = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    project: "ProjectModel" = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    assignments: list["TaskAssignmentModel"] = Relationship(
        back_populates="task",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class TaskAssignmentBase(SQLModel):
    project_task_id: UUID = Field(foreign_key="sprinttask.id", nullable=False)
    project_member_id: UUID = Field(foreign_key="projectmember.id", nullable=False)
    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    accepted_at: datetime | None = None


class TaskAssignmentPublic(BaseModel, TaskAssignmentBase):
    pass


class TaskAssignmentCreate(TaskAssignmentBase):
    pass


class TaskAssignmentUpdate(SQLModel):
    accepted_at: datetime | None = None


class TaskAssignmentModel(TaskAssignmentPublic, table=True):
    __tablename__ = "taskassignment"

    task: "SprintTaskModel" = Relationship(
        back_populates="assignments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    project_member: "ProjectMemberModel" = Relationship(
        back_populates="assignments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    busy_slots: list["BusySlotModel"] = Relationship(
        back_populates="task_assignment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    change_requests: list["TaskChangeRequestModel"] = Relationship(
        back_populates="task_assignment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class TaskChangeRequestBase(SQLModel):
    task_assignment_id: UUID = Field(foreign_key="taskassignment.id", nullable=False)
    requested_by_member_id: UUID = Field(
        foreign_key="projectmember.id", nullable=False
    )
    reason: str | None = Field(default=None, sa_column=Column(Text))
    status: TaskChangeRequestStatus = Field(
        default=TaskChangeRequestStatus.PENDING, nullable=False
    )
    handled_at: datetime | None = None


class TaskChangeRequestPublic(BaseModel, TaskChangeRequestBase):
    pass


class TaskChangeRequestCreate(TaskChangeRequestBase):
    pass


class TaskChangeRequestUpdate(SQLModel):
    status: TaskChangeRequestStatus | None = None
    reason: str | None = None
    handled_at: datetime | None = None


class TaskChangeRequestModel(TaskChangeRequestPublic, table=True):
    __tablename__ = "taskchangerequest"

    task_assignment: "TaskAssignmentModel" = Relationship(
        back_populates="change_requests",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    requested_by_member: "ProjectMemberModel" = Relationship(
        back_populates="change_requests",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
