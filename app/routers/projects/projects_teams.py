from uuid import UUID

from fastapi import APIRouter, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import TeamServiceDep
from app.models.projects.team import TeamCreate, TeamPublic
from app.schemas.projects import TeamFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/projects/{project_id}',
    tags=['projects'],
    responses=get_responses(status.HTTP_404_NOT_FOUND)
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
        raise ForbiddenError()

    filters.project_id = project_id
    return await team_service.get_teams(filters)


@router.post(
    '/teams', status_code=status.HTTP_201_CREATED,
    responses=get_responses(status.HTTP_400_BAD_REQUEST))
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
        raise ForbiddenError()

    team_create.project_id = project_id
    return await team_service.create_team(team_create)
