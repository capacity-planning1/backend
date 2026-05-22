from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import TaskChangeRequestServiceDep
from app.models.sprints.task_change_request import (
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
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    filters: TaskChangeRequestFilters,
) -> Sequence[TaskChangeRequestPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    return await task_change_request_service.get_task_change_requests(
        filters, project_id
    )


@router.post('/tasks/{task_id}/change-requests')
async def create_task_change_request(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    task_id: UUID,
    task_change_request_create: TaskChangeRequestCreate,
) -> TaskChangeRequestPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    task_change_request_create.task_assignment_id = task_id
    return await task_change_request_service.create_task_change_request(
        task_change_request_create
    )


@router.get('/change-requests/{request_id}')
async def get_task_change_request(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    request_id: UUID,
) -> Optional[TaskChangeRequestPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    task_change_request = await task_change_request_service.get_task_change_request(request_id)

    if (
        student.id != task_change_request.requested_by_member_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return task_change_request


@router.put('/change-requests/{request_id}')
async def update_task_change_request(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    request_id: UUID,
    task_change_request_update: TaskChangeRequestUpdate,
) -> Optional[TaskChangeRequestPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    task_change_request = await task_change_request_service.get_task_change_request(
        request_id)

    if (
        student.id != task_change_request.requested_by_member_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await task_change_request_service.update_task_change_request(
        request_id, task_change_request_update)


@router.delete('/change-requests/{request_id}')
async def delete_task_change_request(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    request_id: UUID,
) -> Optional[TaskChangeRequestPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status=status.HTTP_403_FORBIDDEN)

    task_change_request = await task_change_request_service.get_task_change_request(
        request_id)

    if (
        student.id != task_change_request.requested_by_member_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await task_change_request_service.delete_task_change_request(request_id)
