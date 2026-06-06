from typing import Optional
from uuid import UUID

from app.dependencies.repositories import (
    SprintRepository,
    SprintRepositoryDep,
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
from app.utils.errors import NotFoundError
from app.utils.pagination import ListResponse


class SprintTaskService:
    __sprint_task_repository: SprintTaskRepository
    __sprint_repository: SprintRepository

    def __init__(
        self,
        sprint_task_repository: SprintTaskRepositoryDep,
        sprint_repository: SprintRepositoryDep,
    ):
        self.__sprint_task_repository = sprint_task_repository
        self.__sprint_repository = sprint_repository

    async def get_tasks(
        self, filters: SprintTaskFilters
    ) -> ListResponse[SprintTaskPublic]:
        sprint = await self.__sprint_repository.get(filters.sprint_id)
        if sprint is None:
            raise NotFoundError()
        return await self.__sprint_task_repository.fetch(filters)

    async def create_task(self, task_create: SprintTaskCreate) -> SprintTaskPublic:
        task_dump = task_create.model_dump()
        task = SprintTaskModel(**task_dump)
        return await self.__sprint_task_repository.save(task)

    async def get_task(self, task_id: UUID) -> Optional[SprintTaskPublic]:
        result = await self.__sprint_task_repository.get(task_id)
        if result is None:
            raise NotFoundError()
        return result

    async def update_task(
        self, task_id: UUID, task_update: SprintTaskUpdate
    ) -> Optional[SprintTaskPublic]:
        result = await self.__sprint_task_repository.update(task_id, task_update)
        if result is None:
            raise NotFoundError()
        return result

    async def delete_task(self, task_id: UUID) -> Optional[SprintTaskPublic]:
        result = await self.__sprint_task_repository.delete(task_id)
        if result is None:
            raise NotFoundError()
        return result
