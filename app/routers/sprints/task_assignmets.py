from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import TaskAssignmentServiceDep
from app.models.sprints import (
    TaskAssignmentCreate,
    TaskAssignmentPublic,
    TaskAssignmentUpdate,
)
from app.schemas.sprints import TaskAssignmentFilters

router = APIRouter(
    prefix='/tasks/{task_id}/assignments',
    tags=['task_assignment'],
)


@router.get('/')
async def get_task_assignments(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    filters: TaskAssignmentFilters,
) -> Sequence[TaskAssignmentPublic]:
    filters.project_task_id = task_id
    return await task_assignment_service.get_task_assignments(filters)


@router.post('/')
async def create_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    task_assignment_create: TaskAssignmentCreate,
) -> TaskAssignmentPublic:
    task_assignment_create.project_task_id = task_id
    return await task_assignment_service.create_task_assignment(task_assignment_create)


@router.get('/{project_member_id}')
async def get_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    project_member_id: UUID,
) -> Optional[TaskAssignmentPublic]:
    filters = TaskAssignmentFilters()
    filters.project_member_id = project_member_id
    filters.project_task_id = task_id
    return await task_assignment_service.get_task_assignment(filters)


@router.put('/{project_member_id}')
async def update_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    project_member_id: UUID,
    task_assignment_update: TaskAssignmentUpdate,
) -> Optional[TaskAssignmentPublic]:
    filters = TaskAssignmentFilters()
    filters.project_task_id = task_id
    filters.project_member_id = project_member_id
    return await task_assignment_service.update_task_assignment(
        filters, task_assignment_update
    )


@router.delete('/{project_member_id}')
async def delete_task_assignment(
    task_assignment_service: TaskAssignmentServiceDep,
    project_id: UUID,
    task_id: UUID,
    project_member_id: UUID,
) -> Optional[TaskAssignmentPublic]:
    filters = TaskAssignmentFilters()
    filters.project_task_id = task_id
    filters.project_member_id = project_member_id
    return await task_assignment_service.delete_task_assignment(
        task_id, project_member_id
    )
