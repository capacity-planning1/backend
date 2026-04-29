from uuid import UUID
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.base import BaseModel
    from app.models.projects.team import TeamModel
    from app.models.projects.project_member import ProjectMemberModel


class TeamMembershipBase(SQLModel):
    team_id: UUID = Field(foreign_key='team.id', nullable=False)
    project_member_id: UUID = Field(foreign_key='projectmember.id', nullable=False)
    position: str = Field(nullable=False, max_length=100)


class TeamMembershipPublic(BaseModel, TeamMembershipBase):
    pass


class TeamMembershipCreate(TeamMembershipBase):
    pass


class TeamMembershipUpdate(SQLModel):
    position: str | None = Field(default=None, max_length=100)


class TeamMembershipModel(TeamMembershipPublic, table=True):
    __tablename__ = 'teammembership'

    team: TeamModel = Relationship(
        back_populates="memberships",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    project_member: ProjectMemberModel = Relationship(
        back_populates="team_memberships",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
