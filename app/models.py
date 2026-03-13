from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(index=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)

    registered_at: datetime = Field(default_factory=datetime.utcnow)

    skills: Optional[str] = Field(default=None)


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner_student_id: int = Field(foreign_key="student.id", nullable=False)


class ProjectMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    project_id: int = Field(foreign_key="project.id", nullable=False)
    student_id: int = Field(foreign_key="student.id", nullable=False)

    role: str = Field(nullable=False)

    join_date: date = Field(default_factory=date.today)

    is_active: bool = Field(default=True)


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    project_id: int = Field(foreign_key="project.id", nullable=False)

    name: str = Field(nullable=False)

    description: Optional[str] = Field(default=None)


class TeamMembership(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    team_id: int = Field(foreign_key="team.id", nullable=False)

    project_member_id: int = Field(foreign_key="projectmember.id", nullable=False)

    position: str = Field(nullable=False)