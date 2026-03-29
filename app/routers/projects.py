from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import (
    ProjectMemberServiceDep,
    ProjectServiceDep,
    TeamMembershipServiceDep,
    TeamServiceDep,
)
from app.models.projects import (
    ProjectCreate,
    ProjectMemberCreate,
    ProjectMemberPublic,
    ProjectMemberUpdate,
    ProjectPublic,
    ProjectUpdate,
    TeamCreate,
    TeamMembershipCreate,
    TeamMembershipPublic,
    TeamMembershipUpdate,
    TeamPublic,
    TeamUpdate,
)
from app.schemas.projects import (
    ProjectFilters,
    ProjectMembersFilters,
    TeamFilters,
    TeamMembershipFilters,
)

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)


@router.get('/')
async def get_projects(
    project_service: ProjectServiceDep, filters: Annotated[ProjectFilters, Query()]
) -> Sequence[ProjectPublic]:
    return await project_service.get_projects(filters)


@router.post('/')
async def create_project(
    project_service: ProjectServiceDep, project_create: ProjectCreate
) -> ProjectPublic:
    return await project_service.create_project(project_create)


@router.post('/join')
async def join_project(
    project_member_service: ProjectMemberServiceDep, pm_create: ProjectMemberCreate
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.add_member_to_project(pm_create)


@router.get('/{project_id}')
async def get_project(
    project_service: ProjectServiceDep, project_id: UUID
) -> Optional[ProjectPublic]:
    return await project_service.get_project(project_id)


@router.put('/{project_id}')
async def update_project(
    project_service: ProjectServiceDep, project_update: ProjectUpdate, project_id: UUID
) -> Optional[ProjectPublic]:
    return await project_service.update_project(project_update, project_id)


@router.delete('/{project_id}')
async def detele_project(
    project_member_service: ProjectServiceDep, project_id: UUID
) -> Optional[ProjectPublic]:
    return await project_member_service.delete_project(project_id)


@router.get('/{project_id}/members')
async def get_project_members(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    filters: ProjectMembersFilters,
) -> Sequence[ProjectMemberPublic]:
    filters.project_id = project_id
    return await project_member_service.get_projects_members(filters)


@router.post('/{project_id}/members')
async def create_project_members(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    pm_create: ProjectMemberCreate,
) -> ProjectMemberPublic:
    pm_create.project_id = project_id
    return await project_member_service.add_member_to_project(pm_create)


@router.get('/{project_id}/members/{student_id}')
async def get_project_member(
    project_member_service: ProjectMemberServiceDep, project_id: UUID, student_id: UUID
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.get_project_member(student_id, project_id)


@router.put('/{project_id}/members/{student_id}')
async def update_project_member(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
    project_member_update: ProjectMemberUpdate,
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.update_project_member(
        project_id, student_id, project_member_update
    )


@router.delete('/{project_id}/members/{student_id}')
async def delete_project_member(
    project_member_service: ProjectMemberServiceDep, project_id: UUID, student_id: UUID
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.delete_project_member(project_id, student_id)


@router.get('/{project_id}/teams')
async def get_teams(
    team_service: TeamServiceDep, project_id: UUID, filters: TeamFilters
) -> Sequence[TeamPublic]:
    filters.project_id = project_id
    return await team_service.get_teams(filters)


@router.post('/{project_id}/teams')
async def create_team(
    team_service: TeamServiceDep, project_id: UUID, team_create: TeamCreate
) -> TeamPublic:
    team_create.project_id = project_id
    return await team_service.create_team(team_create)


@router.get('/{project_id}/teams/{team_id}')
async def get_team(
    team_service: TeamServiceDep, project_id: UUID, team_id: UUID
) -> Optional[TeamPublic]:
    return await team_service.get_team(team_id)


@router.put('/{project_id}/teams/{team_id}')
async def update_team(
    team_service: TeamServiceDep,
    project_id: UUID,
    team_id: UUID,
    team_update: TeamUpdate,
) -> Optional[TeamPublic]:
    return await team_service.update_team(team_id, team_update)


@router.delete('/{project_id}/teams/{team_id}')
async def delete_team(
    team_service: TeamServiceDep, team_id: UUID
) -> Optional[TeamPublic]:
    return await team_service.delete_team(team_id)


@router.get('{project_id}/teams/{team_id}/members')
async def get_team_members(
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    filters: TeamMembershipFilters,
) -> Sequence[TeamMembershipPublic]:
    filters.team_id = team_id
    return await team_membership_service.get_members(filters)


@router.post('{project_id}/teams/{team_id}/members')
async def create_team_member(
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    tm_create: TeamMembershipCreate,
) -> TeamMembershipPublic:
    tm_create.team_id = team_id
    return await team_membership_service.create_membership(tm_create)


@router.get('{project_id}/teams/{team_id}/members/{student_id}')
async def get_member(
    team_membership_service: TeamMembershipServiceDep, team_id: UUID, student_id: UUID
) -> Optional[TeamMembershipPublic]:
    return await team_membership_service.get_member(team_id, student_id)


@router.put('{project_id}/teams/{team_id}/members/{student_id}')
async def update_team_member(
    team_membership_service: TeamMembershipServiceDep,
    team_id: UUID,
    student_id: UUID,
    tm_update: TeamMembershipUpdate,
) -> Optional[TeamMembershipPublic]:
    return await team_membership_service.update_membership(
        team_id, student_id, tm_update
    )


@router.delete('{project_id}/teams/{team_id}/members/{student_id}')
async def delete_membership(
    team_membership_service: TeamMembershipServiceDep, team_id: UUID, student_id: UUID
) -> Optional[TeamMembershipPublic]:
    return await team_membership_service.delete_membership(team_id, student_id)
