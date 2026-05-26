from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import settings
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
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/{project_id}/teams/{team_id}',
    tags=['teams'],
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
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    return await team_service.get_team(team_id)


@router.put('/')
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
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    return await team_service.update_team(team_id, team_update)


@router.delete('/')
async def delete_team(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_service: TeamServiceDep,
    team_id: UUID,
) -> Optional[TeamPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    return await team_service.delete_team(team_id)


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
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)
    filters.team_id = team_id
    return await team_membership_service.get_members(filters)


@router.post('/members')
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
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

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
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)
    filters = TeamMembershipFilters
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.get_member(filters)


@router.put('/members/{student_id}')
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if student.id != student_id or student.role != MemberRole.TEAMLEAD:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.update_membership(filters, tm_update)


@router.delete('/members/{student_id}')
async def delete_membership(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    student_id: UUID,
) -> Optional[TeamMembershipPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.delete_membership(filters)
