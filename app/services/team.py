from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    TeamRepository,
    TeamRepositoryDep,
)
from app.models.projects.team import (
    TeamCreate,
    TeamModel,
    TeamPublic,
    TeamUpdate,
)
from app.schemas.projects import TeamFilters


class TeamService:
    __team_repository: TeamRepository

    def __init__(self, team_repository: TeamRepositoryDep):
        self.__team_repository = team_repository

    async def get_teams(self, filters: TeamFilters) -> Sequence[TeamPublic]:
        return await self.__team_repository.fetch(filters)

    async def create_team(self, team_create: TeamCreate) -> TeamPublic:
        team_dump = team_create.model_dump()
        team = TeamModel(**team_dump)
        return await self.__team_repository.save(team)

    async def get_team(self, team_id: UUID) -> Optional[TeamPublic]:
        return await self.__team_repository.get(team_id)

    async def update_team(
        self, team_id: UUID, team_update: TeamUpdate
    ) -> Optional[TeamPublic]:
        return await self.__team_repository.update(team_id, team_update)

    async def delete_team(self, team_id: UUID) -> Optional[TeamPublic]:
        return await self.__team_repository.delete(team_id)
