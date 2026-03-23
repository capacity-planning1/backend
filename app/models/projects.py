from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

class Project(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class ProjectBase(SQLModel):
    name: str = Field(nullable=False, max_length=255)
    description: str | None = Field(default=None, sa_column=Column(Text))
    owner_student_id: UUID = Field(foreign_key="student.id", nullable=False)


class ProjectPublic(BaseModel, ProjectBase):
    pass


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    owner_student_id: UUID | None = None


class ProjectMember(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    owner: "StudentModel" = Relationship(
        back_populates="owned_projects",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    members: list["ProjectMemberModel"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    teams: list["TeamModel"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    sprints: list["SprintModel"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    tasks: list["SprintTaskModel"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class ProjectMemberBase(SQLModel):
    project_id: UUID = Field(foreign_key="project.id", nullable=False)
    student_id: UUID = Field(foreign_key="student.id", nullable=False)
    role: str = Field(nullable=False, max_length=50)
    join_date: date = Field(default_factory=date.today, nullable=False)
    is_active: bool = Field(default=True, nullable=False)


class ProjectMemberPublic(BaseModel, ProjectMemberBase):
    pass


class Team(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class ProjectMemberUpdate(SQLModel):
    role: str | None = Field(default=None, max_length=50)
    join_date: date | None = None
    is_active: bool | None = None


class ProjectMemberModel(ProjectMemberPublic, table=True):
    __tablename__ = "projectmember"

    project: "ProjectModel" = Relationship(
        back_populates="members",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    student: "StudentModel" = Relationship(
        back_populates="memberships",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    team_memberships: list["TeamMembershipModel"] = Relationship(
        back_populates="project_member",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    assignments: list["TaskAssignmentModel"] = Relationship(
        back_populates="project_member",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    change_requests: list["TaskChangeRequestModel"] = Relationship(
        back_populates="requested_by_member",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class TeamBase(SQLModel):
    project_id: UUID = Field(foreign_key="project.id", nullable=False)
    name: str = Field(nullable=False, max_length=100)
    description: str | None = Field(default=None, sa_column=Column(Text))


class TeamMembership(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = None


class TeamModel(TeamPublic, table=True):
    __tablename__ = "team"

    project: "ProjectModel" = Relationship(
        back_populates="teams",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    memberships: list["TeamMembershipModel"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class TeamMembershipBase(SQLModel):
    team_id: UUID = Field(foreign_key="team.id", nullable=False)
    project_member_id: UUID = Field(foreign_key="projectmember.id", nullable=False)
    position: str = Field(nullable=False, max_length=100)


class TeamMembershipPublic(BaseModel, TeamMembershipBase):
    pass


class TeamMembershipCreate(TeamMembershipBase):
    pass


class TeamMembershipUpdate(SQLModel):
    position: str | None = Field(default=None, max_length=100)


class TeamMembershipModel(TeamMembershipPublic, table=True):
    __tablename__ = "teammembership"

    team: "TeamModel" = Relationship(
        back_populates="memberships",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    project_member: "ProjectMemberModel" = Relationship(
        back_populates="team_memberships",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
