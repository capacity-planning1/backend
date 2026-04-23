from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import SprintServiceDep
from app.models.sprints import (
    SprintCreate,
    SprintPublic,
    SprintUpdate,
)
from app.routers.sprints import (
    project_tasks,
    task_assignmets,
    task_change_request,
)
from app.schemas.sprints import SprintFilters

router = APIRouter(
    prefix='/projects/{project_id}/sprints',
    tags=['sprints'],
)

router.include_router(task_assignmets.router)
router.include_router(task_change_request.router)
router.include_router(project_tasks.router)


@router.get('/')
async def get_sprints(
    sprint_service: SprintServiceDep, project_id: UUID, filters: SprintFilters
) -> Sequence[SprintPublic]:
    filters.project_id = project_id
    return await sprint_service.get_sprints(filters)


@router.post('/')
async def create_sprint(
    sprint_service: SprintServiceDep, sprint_create: SprintCreate, project_id: UUID
) -> SprintPublic:
    sprint_create.project_id = project_id
    return await sprint_service.create_sprint(sprint_create)


@router.get('/{sprint_id}')
async def get_sprint(
    sprint_service: SprintServiceDep, project_id: UUID, sprint_id: UUID
) -> Optional[SprintPublic]:
    return await sprint_service.get_sprint(sprint_id)


@router.put('/{sprint_id}')
async def update_sprint(
    sprint_service: SprintServiceDep,
    project_id: UUID,
    sprint_id: UUID,
    sprint_update: SprintUpdate,
) -> Optional[SprintPublic]:
    return await sprint_service.update_sprint(sprint_update, sprint_id)


@router.delete('/{sprint_id}')
async def delete_sprint(
    sprint_service: SprintServiceDep, project_id: UUID, sprint_id: UUID
) -> Optional[SprintPublic]:
    return await sprint_service.delete_sprint(sprint_id)
