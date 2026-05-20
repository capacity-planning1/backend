from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.auth import CurrentStudentDep
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

router = APIRouter(
    prefix='/{project_id}/teams/{team_id}',
    tags=['teams'],
)


@router.get('/')
async def get_team(
    _role: CurrentStudentDep,
    team_service: TeamServiceDep, _project_id: UUID, team_id: UUID
) -> Optional[TeamPublic]:
    return await team_service.get_team(team_id)


@router.put('/')
async def update_team(
    _role: CurrentStudentDep,
    team_service: TeamServiceDep,
    _project_id: UUID,
    team_id: UUID,
    team_update: TeamUpdate,
) -> Optional[TeamPublic]:
    return await team_service.update_team(team_id, team_update)


@router.delete('/')
async def delete_team(
    _role: CurrentStudentDep,
    team_service: TeamServiceDep,
    _project_id: UUID,
    team_id: UUID,
) -> Optional[TeamPublic]:
    return await team_service.delete_team(team_id)


@router.get('/members')
async def get_team_members(
    _role: CurrentStudentDep,
    team_membership_service: TeamMembershipServiceDep,
    _project_id: UUID,
    team_id: UUID,
    filters: TeamMembershipFilters,
) -> Sequence[TeamMembershipPublic]:
    filters.team_id = team_id
    return await team_membership_service.get_members(filters)


@router.post('/members')
async def create_team_member(
    _role: CurrentStudentDep,
    team_membership_service: TeamMembershipServiceDep,
    _project_id: UUID,
    team_id: UUID,
    tm_create: TeamMembershipCreate,
) -> TeamMembershipPublic:
    tm_create.team_id = team_id
    return await team_membership_service.create_membership(tm_create)


@router.get('/members/{student_id}')
async def get_member(
    _role: CurrentStudentDep,
    team_membership_service: TeamMembershipServiceDep,
    _project_id: UUID,
    team_id: UUID,
    student_id: UUID,
) -> Optional[TeamMembershipPublic]:
    filters = TeamMembershipFilters
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.get_member(filters)


@router.put('/members/{student_id}')
async def update_team_member(
    _student: CurrentStudentDep,
    team_membership_service: TeamMembershipServiceDep,
    _project_id: UUID,
    team_id: UUID,
    student_id: UUID,
    tm_update: TeamMembershipUpdate,
) -> Optional[TeamMembershipPublic]:
    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.update_membership(filters, tm_update)


@router.delete('/members/{student_id}')
async def delete_membership(
    _student: CurrentStudentDep,
    team_membership_service: TeamMembershipServiceDep,
    _project_id: UUID,
    team_id: UUID,
    student_id: UUID,
) -> Optional[TeamMembershipPublic]:
    filters = TeamMembershipFilters()
    filters.team_id = team_id
    filters.project_member_id = student_id
    return await team_membership_service.delete_membership(filters)
