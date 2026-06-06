from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import (
    CurrentStudentDep,
    MemberRole,
    ProjectRoleDep,
    get_current_student,
)
from app.dependencies.services import (
    ProjectMemberServiceDep,
    ProjectServiceDep,
)
from app.models.projects.project import (
    ProjectCreate,
    ProjectPublic,
    ProjectUpdate,
)
from app.models.projects.project_member import (
    ProjectMemberCreate,
    ProjectMemberPublic,
)
from app.routers.projects import projects_members, projects_team, projects_teams
from app.schemas.projects import ProjectFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
    responses=get_responses(status.HTTP_403_FORBIDDEN),
)

router.include_router(projects_team.router)
router.include_router(projects_teams.router)
router.include_router(projects_members.router)


@router.get('/', dependencies=[Depends(get_current_student)])
async def get_projects(
    _request: Request,
    project_service: ProjectServiceDep,
    filters: Annotated[ProjectFilters, Depends()],
) -> ListResponse[ProjectPublic]:
    return await project_service.get_projects(filters)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_student)],
    responses=get_responses(status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND),
)
async def create_project(
    _request: Request, project_service: ProjectServiceDep, project_create: ProjectCreate
) -> ProjectPublic:
    return await project_service.create_project(project_create)


@router.post(
    '/join',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_student)],
    responses=get_responses(
        status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND, status.HTTP_409_CONFLICT
    ),
)
async def join_project(
    _request: Request,
    project_member_service: ProjectMemberServiceDep,
    pm_create: ProjectMemberCreate,
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.add_member_to_project(pm_create)


@router.get(
    '/{project_id}',
    dependencies=[Depends(get_current_student)],
    responses=get_responses(status.HTTP_404_NOT_FOUND),
)
async def get_project(
    _request: Request, project_service: ProjectServiceDep, project_id: UUID
) -> Optional[ProjectPublic]:
    return await project_service.get_project(project_id)


@router.put(
    '/{project_id}',
    responses=get_responses(status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND),
)
async def update_project(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_service: ProjectServiceDep,
    project_update: ProjectUpdate,
    project_id: UUID,
) -> Optional[ProjectPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    return await project_service.update_project(project_update, project_id)


@router.delete(
    '/{project_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses=get_responses(status.HTTP_404_NOT_FOUND),
)
async def detele_project(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectServiceDep,
    project_id: UUID,
):
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise ForbiddenError()

    await project_member_service.delete_project(project_id)
