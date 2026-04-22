from typing import Optional, Sequence

from app.dependencies.repositories import (
    TeamMembershipRepository,
    TeamMembershipRepositoryDep,
)
from app.models.projects.project import (
    TeamMembershipCreate,
    TeamMembershipModel,
    TeamMembershipPublic,
    TeamMembershipUpdate,
)
from app.schemas.projects import TeamMembershipFilters


class TeamMembershipService:
    __team_membership_repository: TeamMembershipRepository

    def __init__(self, tm_repository: TeamMembershipRepositoryDep):
        self.__team_membership_repository = tm_repository

    async def get_members(
        self, filters: TeamMembershipFilters
    ) -> Sequence[TeamMembershipPublic]:
        return await self.__team_membership_repository.fetch(filters)

    async def create_membership(
        self, tm_create: TeamMembershipCreate
    ) -> TeamMembershipPublic:
        tm_dump = tm_create.model_dump()
        tm = TeamMembershipModel(**tm_dump)
        return await self.__team_membership_repository.save(tm)

    async def get_member(
        self, filters: TeamMembershipFilters
    ) -> Optional[TeamMembershipPublic]:
        result = await self.__team_membership_repository.fetch(filters)

        if len(result) == 0:
            return None

        return result[0]

    async def update_membership(
        self, filters: TeamMembershipFilters, tm_update: TeamMembershipUpdate
    ) -> Optional[TeamMembershipPublic]:
        tm = await self.__team_membership_repository.fetch(filters)

        if len(tm) == 0:
            return None

        return await self.__team_membership_repository.update(tm[0].id, tm_update)

    async def delete_membership(
        self, filters: TeamMembershipFilters
    ) -> Optional[TeamMembershipPublic]:
        tm = await self.__team_membership_repository.fetch(filters)

        if len(tm) == 0:
            return None

        return await self.__team_membership_repository.delete(tm[0].id)
