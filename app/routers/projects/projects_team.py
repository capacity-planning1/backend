from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import (
    TeamMembershipServiceDep,
    TeamServiceDep,
)
from app.models.projects.team import (
    TeamPublic,
    TeamUpdate,
)
from app.models.projects.team_membership import (
    TeamMembershipCreate,
    TeamMembershipPublic,
    TeamMembershipUpdate,
)
from app.schemas.projects import TeamMembershipFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/{project_id}/teams/{team_id}',
    tags=['teams'],
    responses=get_responses(status.HTTP_404_NOT_FOUND),
)


@router.get('/')
async def get_team(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_service: TeamServiceDep,
    team_id: UUID,
) -> ListResponse[TeamPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    return await team_service.get_team(team_id)


@router.put('/', responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def update_team(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_service: TeamServiceDep,
    team_id: UUID,
    team_update: TeamUpdate,
) -> Optional[TeamPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    return await team_service.update_team(team_id, team_update)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_service: TeamServiceDep,
    team_id: UUID,
):
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    await team_service.delete_team(team_id)


@router.get('/members')
async def get_team_members(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    filters: TeamMembershipFilters,
) -> ListResponse[TeamMembershipPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()
    filters.team_id = team_id
    return await team_membership_service.get_members(filters)


@router.post(
    '/members',
    status_code=status.HTTP_201_CREATED,
    responses=get_responses(status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT),
)
async def create_team_member(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    tm_create: TeamMembershipCreate,
) -> TeamMembershipPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    tm_create.team_id = team_id
    return await team_membership_service.create_membership(tm_create)


@router.get('/members/{student_id}')
async def get_member(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    student_id: UUID,
) -> Optional[TeamMembershipPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()
    filters = TeamMembershipFilters
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.get_member(filters)


@router.put(
    '/members/{student_id}',
    responses=get_responses(status.HTTP_400_BAD_REQUEST),
)
async def update_team_member(  # noqa: PLR0913
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    student_id: UUID,
    tm_update: TeamMembershipUpdate,
) -> Optional[TeamMembershipPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    if student.id != student_id or student.role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.update_membership(filters, tm_update)


@router.delete('/members/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_membership(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    student_id: UUID,
):
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    await team_membership_service.delete_membership(filters)
