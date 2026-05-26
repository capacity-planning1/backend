from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import settings
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import TeamServiceDep
from app.models.projects.team import TeamCreate, TeamPublic
from app.schemas.projects import TeamFilters
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/projects/{project_id}',
    tags=['projects'],
)


@router.get('/teams')
async def get_teams(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_service: TeamServiceDep,
    project_id: UUID,
    filters: TeamFilters,
) -> ListResponse[TeamPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters.project_id = project_id
    return await team_service.get_teams(filters)


@router.post('/teams')
async def create_team(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_service: TeamServiceDep,
    project_id: UUID,
    team_create: TeamCreate,
) -> TeamPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    team_create.project_id = project_id
    return await team_service.create_team(team_create)
