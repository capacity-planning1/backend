from typing import Optional
from uuid import UUID

from app.dependencies.repositories import ProjectRepository, ProjectRepositoryDep
from app.models.projects.project import (
    ProjectCreate,
    ProjectModel,
    ProjectPublic,
    ProjectUpdate,
)
from app.schemas.projects import ProjectFilters
from app.utils.pagination import ListResponse


class ProjectService:
    __project_repository: ProjectRepository

    def __init__(
        self,
        project_repository: ProjectRepositoryDep,
    ):
        self.__project_repository = project_repository

    async def get_projects(
        self, filters: ProjectFilters
    ) -> ListResponse[ProjectPublic]:
        return await self.__project_repository.fetch(filters)

    async def create_project(self, project_create: ProjectCreate) -> ProjectPublic:
        project_dump = project_create.model_dump()
        project = ProjectModel(**project_dump)
        return await self.__project_repository.save(project)

    async def get_project(self, project_id: UUID) -> Optional[ProjectPublic]:
        return await self.__project_repository.get(project_id)

    async def update_project(
        self, project_update: ProjectUpdate, project_id: UUID
    ) -> Optional[ProjectModel]:
        return await self.__project_repository.update(project_id, project_update)

    async def delete_project(self, project_id: UUID) -> Optional[ProjectPublic]:
        return await self.__project_repository.delete(project_id)
