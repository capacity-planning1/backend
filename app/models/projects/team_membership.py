from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.projects.project_member import ProjectMemberModel
    from app.models.projects.team import TeamModel


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

    team: 'TeamModel' = Relationship(
        sa_relationship=relationship(
            "TeamModel",
            back_populates='memberships',
            lazy="selectin",
        )
    )
    project_member: 'ProjectMemberModel' = Relationship(
        sa_relationship=relationship(
            "ProjectMemberModel",
            back_populates='team_memberships',
            lazy="selectin",
        )
    )
