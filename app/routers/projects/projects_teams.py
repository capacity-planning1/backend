from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import TeamServiceDep
from app.models.projects.team import TeamCreate, TeamPublic
from app.schemas.projects import TeamFilters

router = APIRouter(
    prefix='/projects/{project_id}',
    tags=['projects'],
)


@router.get('/teams')
async def get_teams(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    team_service: TeamServiceDep,
    project_id: UUID,
    filters: TeamFilters,
) -> Sequence[TeamPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters.project_id = project_id
    return await team_service.get_teams(filters)


@router.post('/teams')
async def create_team(
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
