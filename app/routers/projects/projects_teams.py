from typing import Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.auth import CurrentStudentDep
from app.dependencies.services import TeamServiceDep
from app.models.projects.team import TeamCreate, TeamPublic
from app.schemas.projects import TeamFilters

router = APIRouter(
    prefix='/projects/{project_id}',
    tags=['projects'],
)


@router.get('/teams')
async def get_teams(
    _role: CurrentStudentDep,
    team_service: TeamServiceDep,
    project_id: UUID,
    filters: TeamFilters,
) -> Sequence[TeamPublic]:
    filters.project_id = project_id
    return await team_service.get_teams(filters)


@router.post('/teams')
async def create_team(
    _role: CurrentStudentDep,
    team_service: TeamServiceDep,
    project_id: UUID,
    team_create: TeamCreate,
) -> TeamPublic:
    team_create.project_id = project_id
    return await team_service.create_team(team_create)
