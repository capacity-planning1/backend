from typing import Optional

from app.dependencies.repositories import (
    TeamMembershipRepository,
    TeamMembershipRepositoryDep,
)
from app.models.projects.team_membership import (
    TeamMembershipCreate,
    TeamMembershipModel,
    TeamMembershipPublic,
    TeamMembershipUpdate,
)
from app.schemas.projects import TeamMembershipFilters
from app.utils.errors import NotFoundError
from app.utils.pagination import ListResponse


class TeamMembershipService:
    __team_membership_repository: TeamMembershipRepository

    def __init__(self, tm_repository: TeamMembershipRepositoryDep):
        self.__team_membership_repository = tm_repository

    async def get_members(
        self, filters: TeamMembershipFilters
    ) -> ListResponse[TeamMembershipPublic]:
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

        if len(result.items) == 0:
            raise NotFoundError()

        return result.items[0]

    async def update_membership(
        self, filters: TeamMembershipFilters, tm_update: TeamMembershipUpdate
    ) -> Optional[TeamMembershipPublic]:
        tm = await self.__team_membership_repository.fetch(filters)

        if len(tm.items) == 0:
            raise NotFoundError()

        return await self.__team_membership_repository.update(tm.items[0].id, tm_update)

    async def delete_membership(
        self, filters: TeamMembershipFilters
    ) -> Optional[TeamMembershipPublic]:
        tm = await self.__team_membership_repository.fetch(filters)

        if len(tm.items) == 0:
            raise NotFoundError()

        return await self.__team_membership_repository.delete(tm.items[0].id)
