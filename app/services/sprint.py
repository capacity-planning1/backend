from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    SprintRepository,
    SprintRepositoryDep,
)
from app.models.sprints import (
    SprintCreate,
    SprintModel,
    SprintPublic,
    SprintUpdate,
)
from app.schemas.sprints import SprintFilters


class SprintService:
    __sprint_repository: SprintRepository

    def __init__(self, sprint_repository: SprintRepositoryDep):
        self.__sprint_repository = sprint_repository

    async def get_sprints(self, filters: SprintFilters) -> Sequence[SprintPublic]:
        return await self.__sprint_repository.fetch(filters)

    async def create_sprint(self, sprint_create: SprintCreate) -> SprintPublic:
        sprint_dump = sprint_create.model_dump()
        sprint = SprintModel(**sprint_dump)
        return await self.__sprint_repository.save(sprint)

    async def get_sprint(self, sprint_id: UUID) -> Optional[SprintPublic]:
        return await self.__sprint_repository.get(sprint_id)

    async def update_sprint(
        self, sprint_update: SprintUpdate, sprint_id: UUID
    ) -> Optional[SprintPublic]:
        return await self.__sprint_repository.update(sprint_id, sprint_update)

    async def delete_sprint(self, sprint_id: UUID) -> Optional[SprintPublic]:
        return await self.__sprint_repository.delete(sprint_id)
