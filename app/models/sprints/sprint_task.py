from __future__ import annotations

from enum import Enum
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


if TYPE_CHECKING:
    from app.models.projects.project import ProjectModel
    from app.models.sprints.sprint import SprintModel
    from app.models.sprints.task_assignment import TaskAssignmentModel


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


class SprintTask(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class SprintTaskBase(SQLModel):
    project_id: UUID = Field(foreign_key='project.id', nullable=False)
    sprint_id: UUID = Field(foreign_key='sprint.id', nullable=False)
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
    __tablename__ = 'sprinttask'

    sprint: SprintModel = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    project: ProjectModel = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    assignments: list[TaskAssignmentModel] = Relationship(
        back_populates="task",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
