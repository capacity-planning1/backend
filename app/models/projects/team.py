from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.projects.project import ProjectModel
    from app.models.projects.team_membership import TeamMembershipModel


class TeamBase(SQLModel):
    project_id: UUID = Field(foreign_key='project.id', nullable=False)
    name: str = Field(nullable=False, max_length=100)
    description: str | None = Field(default=None, sa_column=Column(Text))


class TeamCreate(TeamBase):
    pass


class TeamPublic(BaseModel, TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = None


class TeamModel(TeamPublic, table=True):
    __tablename__ = 'team'

    project: 'ProjectModel' = Relationship(
        sa_relationship=relationship(
            'ProjectModel',
            back_populates='teams',
            lazy='selectin',
        )
    )
    memberships: list['TeamMembershipModel'] = Relationship(
        sa_relationship=relationship(
            'TeamMembershipModel',
            back_populates='team',
            lazy='selectin',
        )
    )
