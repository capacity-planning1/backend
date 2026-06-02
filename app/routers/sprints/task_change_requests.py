from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import TaskChangeRequestServiceDep
from app.models.sprints.task_change_request import (
    TaskChangeRequestCreate,
    TaskChangeRequestPublic,
    TaskChangeRequestUpdate,
)
from app.schemas.sprints import TaskChangeRequestFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='',
    tags=['task_change_request'],
)


@router.get('/change-requests')
async def get_task_change_requests(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    project_id: UUID,
    filters: TaskChangeRequestFilters,
) -> ListResponse[TaskChangeRequestPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    return await task_change_request_service.get_task_change_requests(
        filters, project_id
    )


@router.post(
    '/tasks/{task_id}/change-requests', status_code=status.HTTP_201_CREATED,
    responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def create_task_change_request(
    _request: Request,
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
        raise ForbiddenError()

    task_change_request_create.task_assignment_id = task_id
    return await task_change_request_service.create_task_change_request(
        task_change_request_create
    )


@router.get('/change-requests/{request_id}')
async def get_task_change_request(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    request_id: UUID,
) -> Optional[TaskChangeRequestPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    task_change_request = await task_change_request_service.get_task_change_request(
        request_id
    )

    if (
        student.id != task_change_request.requested_by_member_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    return task_change_request


@router.put(
    '/change-requests/{request_id}',
    responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def update_task_change_request(
    _request: Request,
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
        raise ForbiddenError()

    task_change_request = await task_change_request_service.get_task_change_request(
        request_id
    )

    if (
        student.id != task_change_request.requested_by_member_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    return await task_change_request_service.update_task_change_request(
        request_id, task_change_request_update
    )


@router.delete('/change-requests/{request_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_change_request(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_change_request_service: TaskChangeRequestServiceDep,
    request_id: UUID,
):
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    task_change_request = await task_change_request_service.get_task_change_request(
        request_id
    )

    if (
        student.id != task_change_request.requested_by_member_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    await task_change_request_service.delete_task_change_request(request_id)
