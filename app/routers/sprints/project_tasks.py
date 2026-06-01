from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import SprintTaskServiceDep
from app.models.sprints.sprint_task import (
    SprintTaskCreate,
    SprintTaskPublic,
    SprintTaskUpdate,
)
from app.schemas.sprints import SprintTaskFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/tasks',
    tags=['project_tasks'],
)


@router.get('/')
async def get_tasks(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    filters: SprintTaskFilters,
) -> ListResponse[SprintTaskPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    filters.project_id = project_id
    return await sprint_task_service.get_tasks(filters)


@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    responses=status.HTTP_400_BAD_REQUEST)
async def create_task(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_task_service: SprintTaskServiceDep,
    project_id: UUID,
    task_create: SprintTaskCreate,
) -> SprintTaskPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    task_create.project_id = project_id
    return await sprint_task_service.create_task(task_create)


@router.get('/{task_id}')
async def get_task(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_task_service: SprintTaskServiceDep,
    task_id: UUID,
) -> Optional[SprintTaskPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    return await sprint_task_service.get_task(task_id)


@router.put('/{task_id}', responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def update_task(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_task_service: SprintTaskServiceDep,
    task_id: UUID,
    task_update: SprintTaskUpdate,
) -> Optional[SprintTaskPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    return await sprint_task_service.update_task(task_id, task_update)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_task_service: SprintTaskServiceDep,
    task_id: UUID,
) -> Optional[SprintTaskPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    return await sprint_task_service.delete_task(task_id)
