from typing import Optional

from app.dependencies.repositories import (
    TaskAssignmentRepository,
    TaskAssignmentRepositoryDep,
)
from app.models.sprints.task_assignment import (
    TaskAssignmentCreate,
    TaskAssignmentModel,
    TaskAssignmentPublic,
    TaskAssignmentUpdate,
)
from app.schemas.sprints import TaskAssignmentFilters
from app.utils.pagination import ListResponse


class TaskAssignmentService:
    __task_assignment_repository: TaskAssignmentRepository

    def __init__(self, ta_repository: TaskAssignmentRepositoryDep):
        self.__task_assignment_repository = ta_repository

    async def get_task_assignments(
        self, filters: TaskAssignmentFilters
    ) -> ListResponse[TaskAssignmentPublic]:
        return await self.__task_assignment_repository.fetch(filters)

    async def create_task_assignment(
        self, ta_create: TaskAssignmentCreate
    ) -> TaskAssignmentPublic:
        ta_dump = ta_create.model_dump()
        ta = TaskAssignmentModel(**ta_dump)
        return await self.__task_assignment_repository.save(ta)

    async def get_task_assignment(
        self, filters: TaskAssignmentFilters
    ) -> Optional[TaskAssignmentPublic]:
        result = await self.__task_assignment_repository.fetch(filters)

        if len(result.items) == 0:
            return None

        return result.items[0]

    async def update_task_assignment(
        self, filters: TaskAssignmentFilters, ta_update: TaskAssignmentUpdate
    ) -> Optional[TaskAssignmentPublic]:
        ta = await self.__task_assignment_repository.fetch(filters)

        if len(ta.items) == 0:
            return None

        return await self.__task_assignment_repository.update(ta.items[0].id, ta_update)

    async def delete_task_assignment(
        self, filters: TaskAssignmentFilters
    ) -> Optional[TaskAssignmentPublic]:
        ta = await self.__task_assignment_repository.fetch(filters)

        if len(ta.items) == 0:
            return None

        return await self.__task_assignment_repository.delete(ta.items[0].id)
