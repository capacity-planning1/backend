from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


if TYPE_CHECKING:
    from app.models.project_member import ProjectMemberModel
    from app.models.task_assignment import TaskAssignmentModel


class TaskChangeRequestStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class TaskChangeRequest(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class TaskChangeRequestBase(SQLModel):
    task_assignment_id: UUID = Field(foreign_key='taskassignment.id', nullable=False)
    requested_by_member_id: UUID = Field(foreign_key='projectmember.id', nullable=False)
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
    __tablename__ = 'taskchangerequest'

    task_assignment: TaskAssignmentModel = Relationship(
        back_populates="change_requests",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    requested_by_member: ProjectMemberModel = Relationship(
        back_populates="change_requests",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
