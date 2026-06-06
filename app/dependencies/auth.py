from enum import Enum
from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import app.utils.hasher
from app.core.auth import get_student_id_from_token
from app.dependencies.repositories import (
    ProjectMemberRepositoryDep,
    ProjectRepositoryDep,
    StudentRepositoryDep
)
from app.models.students.student import StudentPublic
from app.schemas.projects import ProjectMembersFilters
from app.utils.errors import NotFoundError, UnauthorizedError

oauth2_scheme = HTTPBearer(auto_error=False)

type AuthenticatedStudent = Optional[StudentPublic]


class MemberRole(str, Enum):
    MEMBER = 'member'
    TEAMLEAD = 'teamlead'
    OTHER = 'other'


async def authenticate_student(
    email: str, password: str, student_repo: StudentRepositoryDep
) -> AuthenticatedStudent:
    student = await student_repo.get_by_email(email)

    if not student:
        return None

    if app.utils.hasher.Hasher.verify_password(password, student.hashed_password):
        return student

    return None


async def get_current_student(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(oauth2_scheme)
    ],
    student_repo: StudentRepositoryDep,
) -> StudentPublic:
    if not credentials:
        raise UnauthorizedError()

    student_id = get_student_id_from_token(credentials.credentials)

    if not student_id:
        raise UnauthorizedError()

    student = await student_repo.get(student_id)
    if not student:
        raise UnauthorizedError()

    return student


CurrentStudentDep = Annotated[StudentPublic, Depends(get_current_student)]


async def get_student_project_role(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(oauth2_scheme)
    ],
    project_repo: ProjectRepositoryDep,
    project_member_repo: ProjectMemberRepositoryDep,
    request: Request,
) -> MemberRole:
    if not credentials:
        raise UnauthorizedError()

    student_id = get_student_id_from_token(credentials.credentials)

    if not student_id:
        raise UnauthorizedError()

    project_id = UUID(request.path_params.get('project_id'))
    project_id_param = request.path_params.get('project_id')
    if not project_id_param:
        return MemberRole.OTHER
    project = await project_repo.get(project_id)

    if not project:
        raise NotFoundError()

    if student_id == project.owner_student_id:
        role = MemberRole.TEAMLEAD
    else:
        filters = ProjectMembersFilters(project_id=project_id)
        project_members = await project_member_repo.fetch(filters)
        is_in_project = False
        for project_member in project_members.items:
            if project_member.student_id == student_id:
                is_in_project = True
        role = MemberRole.MEMBER if is_in_project else MemberRole.OTHER
    return role


ProjectRoleDep = Annotated[MemberRole, Depends(get_student_project_role)]
