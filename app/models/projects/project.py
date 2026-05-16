from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.projects.project_member import ProjectMemberModel
    from app.models.projects.team import TeamModel
    from app.models.sprints.sprint import SprintModel
    from app.models.sprints.sprint_task import SprintTaskModel
    from app.models.students.student import StudentModel


class ProjectBase(SQLModel):
    name: str = Field(nullable=False, max_length=255)
    description: str | None = Field(default=None, sa_column=Column(Text))
    owner_student_id: UUID = Field(foreign_key='student.id', nullable=False)


class ProjectPublic(BaseModel, ProjectBase):
    pass


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    owner_student_id: UUID | None = None


class ProjectModel(ProjectPublic, table=True):
    __tablename__ = 'project'

    owner: 'StudentModel' = Relationship(
        sa_relationship=relationship(
            "StudentModel",
            back_populates='owned_projects',
            lazy="selectin",
        )
    )
    members: list['ProjectMemberModel'] = Relationship(
        sa_relationship=relationship(
            "ProjectMemberModel",
            back_populates='project',
            lazy="selectin",
        )
    )
    teams: list['TeamModel'] = Relationship(
        sa_relationship=relationship(
            "TeamModel",
            back_populates='project',
            lazy="selectin",
        )
    )
    sprints: list['SprintModel'] = Relationship(
        sa_relationship=relationship(
            "SprintModel",
            back_populates='project',
            lazy="selectin",
        )
    )
    tasks: list['SprintTaskModel'] = Relationship(
        sa_relationship=relationship(
            "SprintTaskModel",
            back_populates='project',
            lazy="selectin",
        )
    )
