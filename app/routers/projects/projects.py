from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import (
    ProjectMemberServiceDep,
    ProjectServiceDep,
)
from app.models.projects.project import (
    ProjectCreate,
    ProjectMemberCreate,
    ProjectMemberPublic,
    ProjectPublic,
    ProjectUpdate,
)
from app.routers.projects.projects import (
    projects_members,
    projects_team,
    projects_teams,
)
from app.schemas.projects import ProjectFilters

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)

router.include_router(projects_team.router)
router.include_router(projects_teams.router)
router.include_router(projects_members.router)


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
