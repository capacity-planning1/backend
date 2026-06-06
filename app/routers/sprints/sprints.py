from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import SprintServiceDep
from app.models.sprints.sprint import (
    SprintCreate,
    SprintPublic,
    SprintUpdate,
)
from app.routers.sprints import project_tasks, task_assignmets, task_change_requests
from app.schemas.sprints import SprintFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/projects/{project_id}/sprints',
    tags=['sprints'],
    responses=get_responses(
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND)
)

router.include_router(task_assignmets.router)
router.include_router(task_change_requests.router)
router.include_router(project_tasks.router)


@router.get('/')
async def get_sprints(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep,
    project_id: UUID,
    filters: Annotated[SprintFilters, Depends()],
) -> ListResponse[SprintPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    filters.project_id = project_id
    return await sprint_service.get_sprints(filters)


@router.post(
        '/', status_code=status.HTTP_201_CREATED,
        responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def create_sprint(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep,
    sprint_create: SprintCreate,
    project_id: UUID,
) -> SprintPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    sprint_create.project_id = project_id
    return await sprint_service.create_sprint(sprint_create)


@router.get('/{sprint_id}')
async def get_sprint(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep,
    sprint_id: UUID,
) -> Optional[SprintPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    return await sprint_service.get_sprint(sprint_id)


@router.put('/{sprint_id}', responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def update_sprint(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep,
    sprint_id: UUID,
    sprint_update: SprintUpdate,
) -> Optional[SprintPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    return await sprint_service.update_sprint(sprint_update, sprint_id)


@router.delete('/{sprint_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_sprint(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep,
    sprint_id: UUID,
):
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    await sprint_service.delete_sprint(sprint_id)
