from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import (
    SprintServiceDep,
    SprintTaskServiceDep,
    TaskAssignmentServiceDep,
    TaskChangeRequestServiceDep,
)
from app.models.sprints import (
    SprintCreate,
    SprintPublic,
    SprintTaskCreate,
    SprintTaskPublic,
    SprintTaskUpdate,
    SprintUpdate,
    TaskAssignmentCreate,
    TaskAssignmentPublic,
    TaskAssignmentUpdate,
    TaskChangeRequestCreate,
    TaskChangeRequestPublic,
    TaskChangeRequestUpdate,
)
from app.schemas.sprints import (
    SprintFilters,
    SprintTaskFilters,
    TaskAssignmentFilters,
    TaskChangeRequestFilters,
)

router = APIRouter(
    prefix='/projects',
    tags=['sprints'],
)


@router.get('/{project_id}/sprints')
async def get_sprints(
    sprint_service: SprintServiceDep, project_id: UUID, filters: SprintFilters
) -> Sequence[SprintPublic]:
    filters.project_id = project_id
    return await sprint_service.get_sprints(filters)


@router.post('/{project_id}/sprints')
async def create_sprint(
    sprint_service: SprintServiceDep, sprint_create: SprintCreate, project_id: UUID
) -> SprintPublic:
    sprint_create.project_id = project_id
    return await sprint_service.create_sprint(sprint_create)


@router.get('/{project_id}/sprints/{sprint_id}')
async def get_sprint(
    sprint_service: SprintServiceDep, project_id: UUID, sprint_id: UUID
) -> Optional[SprintPublic]:
    return await sprint_service.get_sprint(sprint_id)


@router.put('/{project_id}/sprints/{sprint_id}')
async def update_sprint(
    sprint_service: SprintServiceDep,
    project_id: UUID,
    sprint_id: UUID,
    sprint_update: SprintUpdate,
) -> Optional[SprintPublic]:
    return await sprint_service.update_sprint(sprint_update, sprint_id)


@router.delete('/{project_id}/sprints/{sprint_id}')
async def delete_sprint(
    sprint_service: SprintServiceDep, project_id: UUID, sprint_id: UUID
) -> Optional[SprintPublic]:
    return await sprint_service.delete_sprint(sprint_id)


@router.get('/{project_id}/tasks')
async def get_tasks(
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    filters: SprintTaskFilters,
) -> Sequence[SprintTaskPublic]:
    filters.project_id = project_id
    return await sprint_task_service.get_tasks(filters)


@router.post('/{project_id}/tasks')
async def create_task(
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    task_create: SprintTaskCreate,
) -> SprintTaskPublic:
    task_create.project_id = project_id
    return await sprint_task_service.create_task(task_create)


@router.get('/{project_id}/tasks/{task_id}')
async def get_task(
    sprint_task_service: SprintTaskServiceDep, project_id: UUID, task_id: UUID
) -> Optional[SprintTaskPublic]:
    return await sprint_task_service.get_task(task_id)


@router.put('/{project_id}/tasks/{task_id}')
async def update_task(
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    task_id: UUID,
    task_update: SprintTaskUpdate,
) -> Optional[SprintTaskPublic]:
    return await sprint_task_service.update_task(task_id, task_update)


@router.delete('/{project_id}/tasks/{task_id}')
async def dekete_task(
    sprint_task_service: SprintTaskServiceDep, project_id: UUID, task_id: UUID
) -> Optional[SprintTaskPublic]:
    return await sprint_task_service.delete_task(task_id)


@router.get('/{project_id}/tasks/{task_id}/assignments')
async def get_task_assignments(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    filters: TaskAssignmentFilters,
) -> Sequence[TaskAssignmentPublic]:
    filters.project_task_id = task_id
    return await task_assignment_service.get_task_assignments(filters)


@router.post('/{project_id}/tasks/{task_id}/assignments')
async def create_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    task_assignment_create: TaskAssignmentCreate,
) -> TaskAssignmentPublic:
    task_assignment_create.project_task_id = task_id
    return await task_assignment_service.create_task_assignment(task_assignment_create)


@router.get('/{project_id}/tasks/{task_id}/assignments/{project_member_id}')
async def get_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    project_member_id: UUID,
) -> Optional[TaskAssignmentPublic]:
    return await task_assignment_service.get_task_assignment(task_id, project_member_id)


@router.put('/{project_id}/tasks/{task_id}/assignments/{project_member_id}')
async def update_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    project_member_id: UUID,
    task_assignment_update: TaskAssignmentUpdate,
) -> Optional[TaskAssignmentPublic]:
    return await task_assignment_service.update_task_assignment(
        task_id, project_member_id, task_assignment_update
    )


@router.delete('/{project_id}/tasks/{task_id}/assignments/{project_member_id}')
async def delete_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    project_member_id: UUID,
) -> Optional[TaskAssignmentPublic]:
    return await task_assignment_service.delete_task_assignment(
        task_id, project_member_id
    )


@router.get('{project_id}/change-requests')
async def get_task_change_requests(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    filters: TaskChangeRequestFilters,
) -> Sequence[TaskChangeRequestPublic]:
    return await task_change_request_service.get_task_change_requests(
        filters, project_id
    )


@router.post('/{project_id}/tasks/{task_id}/change-requests')
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


@router.get('{project_id}/change-requests/{request_id}')
async def get_task_change_request(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    request_id: UUID,
) -> Optional[TaskChangeRequestPublic]:
    return await task_change_request_service.get_task_change_request(request_id)


@router.put('{project_id}/change-requests/{request_id}')
async def update_task_change_request(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    request_id: UUID,
    task_change_request_update: TaskChangeRequestUpdate,
) -> Optional[TaskChangeRequestPublic]:
    return await task_change_request_service.update_task_change_request(
        request_id, task_change_request_update
    )


@router.delete('{project_id}/change-requests/{request_id}')
async def delete_task_change_request(
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    request_id: UUID,
) -> Optional[TaskChangeRequestPublic]:
    return await task_change_request_service.delete_task_change_request(request_id)
