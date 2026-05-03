from __future__ import annotations

from datetime import date
from enum import Enum
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


if TYPE_CHECKING:
    from app.models.projects.project import ProjectModel
    from app.models.sprints.sprint_task import SprintTaskModel


class StatusType(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    REVIEW = 'review'
    TESTING = 'testing'
    DONE = 'done'


class TaskPriority(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'


class TaskChangeRequestStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class SprintBase(SQLModel):
    project_id: UUID = Field(foreign_key='project.id', nullable=False)
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
    __tablename__ = 'sprint'

    project: "ProjectModel" = Relationship(
        back_populates="sprints",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    tasks: list["SprintTaskModel"] = Relationship(
        back_populates="sprint",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
