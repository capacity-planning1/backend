from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


if TYPE_CHECKING:
    from app.models.project_member import ProjectMemberModel
    from app.models.busy_slot import BusySlotModel
    from app.models.task_change_request import TaskChangeRequestModel
    from app.models.sprint_task import SprintTaskModel


class TaskAssignment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class TaskAssignmentBase(SQLModel):
    project_task_id: UUID = Field(foreign_key='sprinttask.id', nullable=False)
    project_member_id: UUID = Field(foreign_key='projectmember.id', nullable=False)
    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    state: str = Field(default="assigned", nullable=False, max_length=50)
    accepted_at: datetime | None = None


class TaskAssignmentCreate(TaskAssignmentBase):
    pass


class TaskAssignmentPublic(TaskAssignmentBase, BaseModel):
    pass


class TaskAssignmentUpdate(SQLModel):
    accepted_at: datetime | None = None


class TaskAssignmentModel(TaskAssignmentPublic, table=True):
    __tablename__ = 'taskassignment'

    task: SprintTaskModel = Relationship(
        back_populates="assignments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    project_member: ProjectMemberModel = Relationship(
        back_populates="assignments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    busy_slots: list[BusySlotModel] = Relationship(
        back_populates="task_assignment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    change_requests: list[TaskChangeRequestModel] = Relationship(
        back_populates="task_assignment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
