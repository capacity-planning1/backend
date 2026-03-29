from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    SprintRepository,
    SprintRepositoryDep,
    SprintTaskRepository,
    SprintTaskRepositoryDep,
    TaskAssignmentRepository,
    TaskAssignmentRepositoryDep,
    TaskChangeRequestRepository,
    TaskChangeRequestRepositoryDep,
)
from app.models.sprints import (
    SprintCreate,
    SprintModel,
    SprintPublic,
    SprintTaskCreate,
    SprintTaskModel,
    SprintTaskPublic,
    SprintTaskUpdate,
    SprintUpdate,
    TaskAssignmentCreate,
    TaskAssignmentModel,
    TaskAssignmentPublic,
    TaskAssignmentUpdate,
    TaskChangeRequestCreate,
    TaskChangeRequestModel,
    TaskChangeRequestPublic,
    TaskChangeRequestUpdate,
)
from app.schemas.sprints import (
    SprintFilters,
    SprintTaskFilters,
    TaskAssignmentFilters,
    TaskChangeRequestFilters,
)


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


class TaskAssignmentService:
    __task_assignment_repository: TaskAssignmentRepository

    def __init__(self, task_assignment_repository: TaskAssignmentRepositoryDep):
        self.__task_assignment_repository = task_assignment_repository

    async def get_task_assignments(
        self, filters: TaskAssignmentFilters
    ) -> Sequence[TaskAssignmentPublic]:
        return await self.__task_assignment_repository.fetch(filters)

    async def get_task_assignment(
        self, task_id: UUID, pm_id: UUID
    ) -> Optional[TaskAssignmentPublic]:
        filters = TaskAssignmentFilters()
        filters.project_task_id = task_id
        filters.project_member_id = pm_id
        result = await self.get_task_assignments(filters)
        if result is None:
            return None

        return result[0]

    async def create_task_assignment(
        self, ta_create: TaskAssignmentCreate
    ) -> TaskAssignmentPublic:
        ta_dump = ta_create.model_dump()
        ta = TaskAssignmentModel(**ta_dump)
        return await self.__task_assignment_repository.save(ta)

    async def update_task_assignment(
        self, task_id: UUID, project_member_id: UUID, ta_update: TaskAssignmentUpdate
    ) -> Optional[TaskAssignmentPublic]:
        filters = TaskAssignmentFilters()
        filters.project_task_id = task_id
        filters.project_member_id = project_member_id

        ta = await self.__task_assignment_repository.fetch(filters)

        if ta is None:
            return None

        return await self.__task_assignment_repository.update(ta[0].id, ta_update)

    async def delete_task_assignment(
        self, task_id: UUID, project_member_id: UUID
    ) -> Optional[TaskAssignmentPublic]:
        filters = TaskAssignmentFilters()
        filters.project_task_id = task_id
        filters.project_member_id = project_member_id

        ta = await self.__task_assignment_repository.fetch(filters)

        if ta is None:
            return None

        return await self.__task_assignment_repository.delete(ta[0].id)


class TaskChangeRequestService:
    __task_change_request_repository: TaskChangeRequestRepository

    def __init__(self, task_change_request__repository: TaskChangeRequestRepositoryDep):
        self.__task_change_request_repository = task_change_request__repository

    async def create_task_change_request(
        self, tcr_create: TaskChangeRequestCreate
    ) -> TaskChangeRequestPublic:
        tcr_dump = tcr_create.model_dump()
        tcr = TaskChangeRequestModel(**tcr_dump)
        return await self.__task_change_request_repository.save(tcr)

    async def get_task_change_request(
        self, tcr_id: UUID
    ) -> Optional[TaskChangeRequestPublic]:
        return await self.__task_change_request_repository.get(tcr_id)

    async def update_task_change_request(
        self, tcr_id: UUID, tcr_update: TaskChangeRequestUpdate
    ) -> Optional[TaskChangeRequestPublic]:
        return await self.__task_change_request_repository.update(tcr_id, tcr_update)

    async def delete_task_change_request(
        self, tcr_id: UUID
    ) -> Optional[TaskChangeRequestPublic]:
        return await self.__task_change_request_repository.delete(tcr_id)

    async def get_task_change_requests(
        self, filters: TaskChangeRequestFilters, project_id: UUID
    ) -> Sequence[TaskChangeRequestPublic]:
        repo = self.__task_change_request_repository
        return await repo.fetch_by_related_project(
            TaskAssignmentModel, 'task_assignment_id', 'project_id', project_id, filters
        )
