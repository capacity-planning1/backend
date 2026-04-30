from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import SprintTaskServiceDep
from app.dependencies.auth import CurrentUserPermissionsDep
from app.models.sprints import (
    SprintTaskCreate,
    SprintTaskPublic,
    SprintTaskUpdate,
)
from app.schemas.sprints import SprintTaskFilters

router = APIRouter(
    prefix='/tasks',
    tags=['project_tasks'],
)


@router.get('/')
async def get_tasks(
    permissions: CurrentUserPermissionsDep,
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    filters: SprintTaskFilters,
) -> Sequence[SprintTaskPublic]:
    filters.project_id = project_id
    return await sprint_task_service.get_tasks(filters)

@router.post('/')
async def create_task(
    permissions: CurrentUserPermissionsDep,
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    task_create: SprintTaskCreate,
) -> SprintTaskPublic:
    task_create.project_id = project_id
    return await sprint_task_service.create_task(task_create)


@router.get('/{task_id}')
async def get_task(
    permissions: CurrentUserPermissionsDep,
    sprint_task_service: SprintTaskServiceDep, project_id: UUID, task_id: UUID
) -> Optional[SprintTaskPublic]:
    return await sprint_task_service.get_task(task_id)


@router.put('/{task_id}')
async def update_task(
    permissions: CurrentUserPermissionsDep,
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    task_id: UUID,
    task_update: SprintTaskUpdate,
) -> Optional[SprintTaskPublic]:
    return await sprint_task_service.update_task(task_id, task_update)


@router.delete('/{task_id}')
async def dekete_task(
    permissions: CurrentUserPermissionsDep,
    sprint_task_service: SprintTaskServiceDep, project_id: UUID, task_id: UUID
) -> Optional[SprintTaskPublic]:
    return await sprint_task_service.delete_task(task_id)
