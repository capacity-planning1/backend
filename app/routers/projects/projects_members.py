from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import ProjectMemberServiceDep
from app.models.projects.project_member import (
    ProjectMemberCreate,
    ProjectMemberPublic,
    ProjectMemberUpdate,
)
from app.schemas.projects import ProjectMembersFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/{project_id}/members',
    tags=['projectMembers'],
    responses=get_responses(status.HTTP_404_NOT_FOUND),
)


@router.get('/')
async def get_project_members(
    _request: Request,
    student: CurrentStudentDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    filters: Annotated[ProjectMembersFilters, Depends()],
    project_role: ProjectRoleDep,
) -> ListResponse[ProjectMemberPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    filters.project_id = project_id
    return await project_member_service.get_project_member(filters)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses=get_responses(status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT),
)
async def create_project_members(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    pm_create: ProjectMemberCreate,
) -> ProjectMemberPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    pm_create.project_id = project_id
    return await project_member_service.add_member_to_project(pm_create)


@router.get('/{student_id}')
async def get_project_member(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
) -> Optional[ProjectMemberPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    filters = ProjectMembersFilters()
    filters.project_id = project_id
    filters.student_id = student_id
    return await project_member_service.get_project_member(filters)


@router.put('/{student_id}', responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def update_project_member(  # noqa: PLR0913
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
    project_member_update: ProjectMemberUpdate,
) -> Optional[ProjectMemberPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    if student.id != student_id or student.role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    filters = ProjectMembersFilters()
    filters.student_id = student_id
    filters.project_id = project_id
    return await project_member_service.update_project_member(
        filters, project_member_update
    )


@router.delete('/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_member(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
):
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    if student.id != student_id or student.role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    filters = ProjectMembersFilters()
    filters.project_id = project_id
    filters.student_id = student_id
    await project_member_service.delete_project_member(filters)
