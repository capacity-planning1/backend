from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import (
    TeamMembershipServiceDep,
    TeamServiceDep,
)
from app.dependencies.auth import CurrentUserPermissionsDep
from app.models.projects.project import (
    TeamMembershipCreate,
    TeamMembershipPublic,
    TeamMembershipUpdate,
    TeamPublic,
    TeamUpdate,
)
from app.schemas.projects import TeamMembershipFilters

router = APIRouter(
    prefix='/{project_id}/teams/{team_id}',
    tags=['teams'],
)


@router.get('/')
async def get_team(
    team_service: TeamServiceDep,
    project_id: UUID,
    team_id: UUID
) -> Optional[TeamPublic]:
    return await team_service.get_team(team_id)


@router.put('/')
async def update_team(
    permissions: CurrentUserPermissionsDep,
    team_service: TeamServiceDep,
    project_id: UUID,
    team_id: UUID,
    team_update: TeamUpdate
) -> Optional[TeamPublic]:
    return await team_service.update_team(team_id, team_update)


@router.delete('/')
async def delete_team(
    permissions: CurrentUserPermissionsDep,
    team_service: TeamServiceDep,
    project_id: UUID,
    team_id: UUID
) -> Optional[TeamPublic]:
    return await team_service.delete_team(team_id)


@router.get('/members')
async def get_team_members(
    team_membership_service: TeamMembershipServiceDep,
    project_id: UUID,
    team_id: UUID,
    filters: TeamMembershipFilters
) -> Sequence[TeamMembershipPublic]:
    filters.team_id = team_id
    return await team_membership_service.get_members(filters)


@router.post('/members')
async def create_team_member(
    permissions: CurrentUserPermissionsDep,
    team_membership_service: TeamMembershipServiceDep,
    project_id: UUID,
    team_id: UUID,
    tm_create: TeamMembershipCreate
) -> TeamMembershipPublic:
    tm_create.team_id = team_id
    return await team_membership_service.create_membership(tm_create)


@router.get('/members/{student_id}')
async def get_member(
    permissions: CurrentUserPermissionsDep,
    team_membership_service: TeamMembershipServiceDep,
    project_id: UUID,
    team_id: UUID,
    student_id: UUID
) -> Optional[TeamMembershipPublic]:
    filters = TeamMembershipFilters
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.get_member(filters)


@router.put('/members/{student_id}')
async def update_team_member(
    permissions: CurrentUserPermissionsDep,
    team_membership_service: TeamMembershipServiceDep,
    project_id: UUID,
    team_id: UUID,
    student_id: UUID,
    tm_update: TeamMembershipUpdate
) -> Optional[TeamMembershipPublic]:
    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.update_membership(
        filters, tm_update)


@router.delete('/members/{student_id}')
async def delete_membership(
    permissions: CurrentUserPermissionsDep,
    team_membership_service: TeamMembershipServiceDep,
    project_id: UUID,
    team_id: UUID,
    student_id: UUID
) -> Optional[TeamMembershipPublic]:
    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.delete_membership(filters)
