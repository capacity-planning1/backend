from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.projects.project_member import ProjectMemberModel
    from app.models.sprints.sprint_task import SprintTaskModel
    from app.models.sprints.task_change_request import TaskChangeRequestModel
    from app.models.students.busy_slot import BusySlotModel


class TaskAssignmentBase(SQLModel):
    project_task_id: UUID = Field(foreign_key='sprinttask.id', nullable=False)
    project_member_id: UUID = Field(foreign_key='projectmember.id', nullable=False)
    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    state: str = Field(default='assigned', nullable=False, max_length=50)
    accepted_at: datetime | None = None


class TaskAssignmentCreate(TaskAssignmentBase):
    pass


class TaskAssignmentPublic(TaskAssignmentBase, BaseModel):
    pass


class TaskAssignmentUpdate(SQLModel):
    accepted_at: datetime | None = None


class TaskAssignmentModel(TaskAssignmentPublic, table=True):
    __tablename__ = 'taskassignment'

    task: 'SprintTaskModel' = Relationship(
        sa_relationship=relationship(
            'SprintTaskModel',
            back_populates='assignments',
            lazy='selectin',
        )
    )
    project_member: 'ProjectMemberModel' = Relationship(
        sa_relationship=relationship(
            'ProjectMemberModel',
            back_populates='assignments',
            lazy='selectin',
        )
    )
    busy_slots: list['BusySlotModel'] = Relationship(
        sa_relationship=relationship(
            'BusySlotModel',
            back_populates='task_assignment',
            lazy='selectin',
        )
    )
    change_requests: list['TaskChangeRequestModel'] = Relationship(
        sa_relationship=relationship(
            'TaskChangeRequestModel',
            back_populates='task_assignment',
            lazy='selectin',
        )
    )
