from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.base import BaseModel
    from app.models.projects.project import ProjectModel
    from app.models.projects.team_membership import TeamMembershipModel


class Team(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class TeamBase(SQLModel):
    project_id: UUID = Field(foreign_key='project.id', nullable=False)
    name: str = Field(nullable=False, max_length=100)
    description: str | None = Field(default=None, sa_column=Column(Text))


class TeamMembership(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class TeamCreate(TeamBase):
    pass


class TeamPublic(BaseModel, TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = None


class TeamModel(TeamPublic, table=True):
    __tablename__ = 'team'

    project: ProjectModel = Relationship(
        back_populates="teams",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    memberships: list[TeamMembershipModel] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
