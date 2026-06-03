from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import TaskAssignmentServiceDep
from app.models.sprints.task_assignment import (
    TaskAssignmentCreate,
    TaskAssignmentPublic,
    TaskAssignmentUpdate,
)
from app.schemas.sprints import TaskAssignmentFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/tasks/{task_id}/assignments',
    tags=['task_assignment'],
)


@router.get('/')
async def get_task_assignments(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_assignment_service: TaskAssignmentServiceDep,
    task_id: UUID,
    filters: TaskAssignmentFilters,
) -> ListResponse[TaskAssignmentPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise ForbiddenError()

    filters.project_task_id = task_id
    return await task_assignment_service.get_task_assignments(filters)


@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def create_task_assignment(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_assignment_service: TaskAssignmentServiceDep,
    task_id: UUID,
    task_assignment_create: TaskAssignmentCreate,
) -> TaskAssignmentPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    task_assignment_create.project_task_id = task_id
    return await task_assignment_service.create_task_assignment(task_assignment_create)


@router.get('/{project_member_id}')
async def get_task_assignment(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_assignment_service: TaskAssignmentServiceDep,
    task_id: UUID,
    project_member_id: UUID,
) -> Optional[TaskAssignmentPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.OTHER
    ):
        raise ForbiddenError()

    if student.id != project_member_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    filters = TaskAssignmentFilters()
    filters.project_member_id = project_member_id
    filters.project_task_id = task_id
    return await task_assignment_service.get_task_assignment(filters)


@router.put(
    '/{project_member_id}',
    responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def update_task_assignment(  # noqa: PLR0913
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_assignment_service: TaskAssignmentServiceDep,
    task_id: UUID,
    project_member_id: UUID,
    task_assignment_update: TaskAssignmentUpdate,
) -> Optional[TaskAssignmentPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.OTHER
    ):
        raise ForbiddenError()

    if student.id != project_member_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    filters = TaskAssignmentFilters()
    filters.project_task_id = task_id
    filters.project_member_id = project_member_id
    return await task_assignment_service.update_task_assignment(
        filters, task_assignment_update
    )


@router.delete('/{project_member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_assignment(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    task_assignment_service: TaskAssignmentServiceDep,
    task_id: UUID,
    project_member_id: UUID,
):
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.OTHER
    ):
        raise ForbiddenError()

    if student.id != project_member_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    filters = TaskAssignmentFilters()
    filters.project_task_id = task_id
    filters.project_member_id = project_member_id
    await task_assignment_service.delete_task_assignment(
        task_id, project_member_id
    )
