from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    SprintTaskRepository,
    SprintTaskRepositoryDep,
)
from app.models.sprints.sprint_task import (
    SprintTaskCreate,
    SprintTaskModel,
    SprintTaskPublic,
    SprintTaskUpdate,
)
from app.schemas.sprints import SprintTaskFilters


class SprintTaskService:
    __sprint_task_repository: SprintTaskRepository

    def __init__(self, sprint_task_repository: SprintTaskRepositoryDep):
        self.__sprint_task_repository = sprint_task_repository

    async def get_tasks(self, filters: SprintTaskFilters) -> Sequence[SprintTaskPublic]:
        return await self.__sprint_task_repository.fetch(filters)

    async def create_task(self, task_create: SprintTaskCreate) -> SprintTaskPublic:
        task_dump = task_create.model_dump()
        task = SprintTaskModel(**task_dump)
        return await self.__sprint_task_repository.save(task)

    async def get_task(self, task_id: UUID) -> Optional[SprintTaskPublic]:
        return await self.__sprint_task_repository.get(task_id)

    async def update_task(
        self, task_id: UUID, task_update: SprintTaskUpdate
    ) -> Optional[SprintTaskPublic]:
        return await self.__sprint_task_repository.update(task_id, task_update)

    async def delete_task(self, task_id: UUID) -> Optional[SprintTaskPublic]:
        return await self.__sprint_task_repository.delete(task_id)
