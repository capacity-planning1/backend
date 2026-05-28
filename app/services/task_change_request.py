from typing import Optional

from app.dependencies.repositories import (
    TaskChangeRequestRepository,
    TaskChangeRequestRepositoryDep,
)
from app.models.sprints.task_change_request import (
    TaskChangeRequestCreate,
    TaskChangeRequestModel,
    TaskChangeRequestPublic,
    TaskChangeRequestUpdate,
)
from app.schemas.sprints import TaskChangeRequestFilters
from app.utils.errors import NotFoundError
from app.utils.pagination import ListResponse


class TaskChangeRequestService:
    __task_change_request_repository: TaskChangeRequestRepository

    def __init__(self, tcr_repository: TaskChangeRequestRepositoryDep):
        self.__task_change_request_repository = tcr_repository

    async def get_task_change_requests(
        self, filters: TaskChangeRequestFilters
    ) -> ListResponse[TaskChangeRequestPublic]:
        return await self.__task_change_request_repository.fetch(filters)

    async def create_task_change_request(
        self, tcr_create: TaskChangeRequestCreate
    ) -> TaskChangeRequestPublic:
        tcr_dump = tcr_create.model_dump()
        tcr = TaskChangeRequestModel(**tcr_dump)
        return await self.__task_change_request_repository.save(tcr)

    async def get_task_change_request(
        self, filters: TaskChangeRequestFilters
    ) -> Optional[TaskChangeRequestPublic]:
        result = await self.__task_change_request_repository.fetch(filters)

        if len(result.items) == 0:
            raise NotFoundError()

        return result.items[0]

    async def update_task_change_request(
        self, filters: TaskChangeRequestFilters, tcr_update: TaskChangeRequestUpdate
    ) -> Optional[TaskChangeRequestPublic]:
        tcr = await self.__task_change_request_repository.fetch(filters)

        if len(tcr.items) == 0:
            raise NotFoundError()

        return await self.__task_change_request_repository.update(
            tcr.items[0].id, tcr_update
        )

    async def delete_task_change_request(
        self, filters: TaskChangeRequestFilters
    ) -> Optional[TaskChangeRequestPublic]:
        tcr = await self.__task_change_request_repository.fetch(filters)

        if len(tcr.items) == 0:
            raise NotFoundError()

        return await self.__task_change_request_repository.delete(tcr.items[0].id)
