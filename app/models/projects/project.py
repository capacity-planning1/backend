from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.base import BaseModel
    from app.models.project_member import ProjectMemberModel
    from app.models.team import TeamModel
    from app.models.student import StudentModel


class Project(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


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

    owner: StudentModel = Relationship(
        back_populates="owned_projects",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    members: list[ProjectMemberModel] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    teams: list[TeamModel] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    sprints: list[SprintModel] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    tasks: list[SprintTaskModel] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
