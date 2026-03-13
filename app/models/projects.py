from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    name: str = Field(nullable=False, max_length=255)

    description: str | None = Field(default=None, sa_column=Column(Text))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    owner_student_id: UUID = Field(foreign_key='student.id', nullable=False)


class ProjectMember(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    project_id: UUID = Field(foreign_key='project.id', nullable=False)

    student_id: UUID = Field(foreign_key='student.id', nullable=False)

    role: str = Field(nullable=False, max_length=50)

    join_date: date = Field(default_factory=date.today)

    is_active: bool = Field(default=True)


class Team(SQLModel, table=True):
    id: UUID = Field(default_factory=UUID, primary_key=True)

    project_id: UUID = Field(foreign_key='project.id', nullable=False)

    name: str = Field(nullable=False, max_length=100)

    description: str | None = Field(default=None, sa_column=Column(Text))


class TeamMembership(SQLModel, table=True):
    id: UUID = Field(default=None, primary_key=True)

    team_id: UUID = Field(foreign_key='team.id', nullable=False)

    project_member_id: UUID = Field(foreign_key='projectmember.id', nullable=False)

    position: str = Field(nullable=False, max_length=100)
