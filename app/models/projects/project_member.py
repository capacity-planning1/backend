from datetime import date
from uuid import UUID
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.base import BaseModel
    from app.models.project import ProjectModel
    from app.models.student import StudentModel
    from app.models.team_membership import TeamMembershipModel
    from app.models.task_assignment import TaskAssignmentModel
    from app.models.task_change_request import TaskChangeRequestModel


class ProjectMemberBase(SQLModel):
    project_id: UUID = Field(foreign_key='project.id', nullable=False)
    student_id: UUID = Field(foreign_key='student.id', nullable=False)
    role: str = Field(nullable=False, max_length=50)
    join_date: date = Field(default_factory=date.today, nullable=False)
    is_active: bool = Field(default=True, nullable=False)


class ProjectMemberPublic(BaseModel, ProjectMemberBase):
    pass


class ProjectMemberUpdate(SQLModel):
    role: str | None = Field(default=None, max_length=50)
    join_date: date | None = None
    is_active: bool | None = None


class ProjectMemberModel(ProjectMemberPublic, table=True):
    __tablename__ = 'projectmember'

    project: ProjectModel = Relationship(
        back_populates="members",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    student: StudentModel = Relationship(
        back_populates="memberships",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    team_memberships: list[TeamMembershipModel] = Relationship(
        back_populates="project_member",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    assignments: list[TaskAssignmentModel] = Relationship(
        back_populates="project_member",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    change_requests: list[TaskChangeRequestModel] = Relationship(
        back_populates="requested_by_member",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
