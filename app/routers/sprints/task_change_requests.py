from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import TaskChangeRequestServiceDep
from app.models.sprints import (
    TaskChangeRequestCreate,
    TaskChangeRequestPublic,
    TaskChangeRequestUpdate,
)
from app.schemas.sprints import TaskChangeRequestFilters

router = APIRouter(
    prefix='',
    tags=['task_change_request'],
)


@router.get('/change-requests')
async def get_task_change_requests(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    filters: TaskChangeRequestFilters,
) -> Sequence[TaskChangeRequestPublic]:
    return await task_change_request_service.get_task_change_requests(
        filters, project_id
    )


@router.post('/tasks/{task_id}/change-requests')
async def create_task_change_request(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    task_id: UUID,
    task_change_request_create: TaskChangeRequestCreate,
) -> TaskChangeRequestPublic:
    task_change_request_create.task_assignment_id = task_id
    return await task_change_request_service.create_task_change_request(
        task_change_request_create
    )


@router.get('/change-requests/{request_id}')
async def get_task_change_request(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    request_id: UUID,
) -> Optional[TaskChangeRequestPublic]:
    return await task_change_request_service.get_task_change_request(request_id)


@router.put('/change-requests/{request_id}')
async def update_task_change_request(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    request_id: UUID,
    task_change_request_update: TaskChangeRequestUpdate,
) -> Optional[TaskChangeRequestPublic]:
    return await task_change_request_service.update_task_change_request(
        request_id, task_change_request_update
    )


@router.delete('/change-requests/{request_id}')
async def delete_task_change_request(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    request_id: UUID,
) -> Optional[TaskChangeRequestPublic]:
    return await task_change_request_service.delete_task_change_request(request_id)
