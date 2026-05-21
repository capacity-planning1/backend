from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import SprintServiceDep
from app.models.sprints.sprint import (
    SprintCreate,
    SprintPublic,
    SprintUpdate,
)
from app.routers.sprints import project_tasks, task_assignmets, task_change_requests
from app.schemas.sprints import SprintFilters

router = APIRouter(
    prefix='/projects/{project_id}/sprints',
    tags=['sprints'],
)

router.include_router(task_assignmets.router)
router.include_router(task_change_requests.router)
router.include_router(project_tasks.router)


@router.get('/')
async def get_sprints(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep, project_id: UUID, filters: SprintFilters
) -> Sequence[SprintPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters.project_id = project_id
    return await sprint_service.get_sprints(filters)


@router.post('/')
async def create_sprint(
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    sprint_create.project_id = project_id
    return await sprint_service.create_sprint(sprint_create)


@router.get('/{sprint_id}')
async def get_sprint(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep,
    sprint_id: UUID,
) -> Optional[SprintPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await sprint_service.get_sprint(sprint_id)


@router.put('/{sprint_id}')
async def update_sprint(
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await sprint_service.update_sprint(sprint_update, sprint_id)


@router.delete('/{sprint_id}')
async def delete_sprint(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    sprint_service: SprintServiceDep,
    sprint_id: UUID,
) -> Optional[SprintPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await sprint_service.delete_sprint(sprint_id)
