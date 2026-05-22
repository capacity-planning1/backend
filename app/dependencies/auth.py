from enum import Enum
from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.auth import get_student_id_from_token
from app.dependencies.repositories import (
    ProjectMemberRepositoryDep,
    ProjectRepositoryDep,
)
from app.dependencies.services import StudentServiceDep
from app.models.students.student import StudentPublic
from app.schemas.projects import ProjectMembersFilters
from app.utils.hasher import Hasher

oauth2_scheme = HTTPBearer(auto_error=False)

type AuthenticatedStudent = Optional[StudentPublic]


class MemberRole(str, Enum):
    MEMBER = 'member'
    TEAMLEAD = 'teamlead'
    OTHER = 'other'


async def authenticate_student(
    email: str, password: str, student_service: StudentServiceDep
) -> AuthenticatedStudent:
    student = await student_service.get_student_by_email(email)

    if not student:
        return None

    if Hasher.verify_password(password, student.hashed_password):
        return student

    return None


async def get_current_student(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(oauth2_scheme)
    ],
    student_service: StudentServiceDep,
) -> StudentPublic:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated'
        )

    student_id = get_student_id_from_token(credentials.credentials)

    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token'
        )

    student = await student_service.get_student(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found'
        )

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated'
        )

    student_id = get_student_id_from_token(credentials.credentials)

    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token'
        )

    project_id = UUID(request.path_params.get('project_id'))
    project = await project_repo.get(project_id)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if student_id == project.owner_student_id:
        role = MemberRole.TEAMLEAD
    else:
        filters = ProjectMembersFilters(project_id=project_id)
        project_members = await project_member_repo.fetch(filters)
        is_in_project = False
        for project_member in project_members:
            if project_member.student_id == student_id:
                is_in_project = True
        role = MemberRole.MEMBER if is_in_project else MemberRole.OTHER
    return role


ProjectRoleDep = Annotated[MemberRole, Depends(get_student_project_role)]
