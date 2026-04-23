from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    ProjectMemberRepository,
    ProjectMemberRepositoryDep,
)
from app.models.projects.project_member import (
    ProjectMemberCreate,
    ProjectMemberModel,
    ProjectMemberPublic,
    ProjectMemberUpdate,
)
from app.schemas.projects import ProjectMembersFilters


class ProjectMemberService:
    __project_member_repository: ProjectMemberRepository

    def __init__(
        self,
        project_member_repository: ProjectMemberRepositoryDep,
    ):
        self.__project_member_repository = project_member_repository

    async def add_member_to_project(
        self, project_member_create: ProjectMemberCreate
    ) -> ProjectMemberPublic:
        project_member_dump = project_member_create.model_dump()
        project_member = ProjectMemberModel(**project_member_dump)
        return await self.__project_member_repository.save(project_member)

    async def get_projects_members(
        self, filters: ProjectMembersFilters
    ) -> Sequence[ProjectMemberPublic]:
        return await self.__project_member_repository.fetch(filters)

    async def get_project_member(
        self, filters: ProjectMembersFilters
    ) -> Optional[ProjectMemberPublic]:
        result = await self.__project_member_repository.fetch(filters)

        if len(result) == 0:
            return None

        return result[0]

    async def update_project_member(
        self, filters: ProjectMembersFilters, pm_update: ProjectMemberUpdate
    ) -> Optional[ProjectMemberPublic]:
        pm = await self.__project_member_repository.fetch(filters)

        if len(pm) == 0:
            return None

        return await self.__project_member_repository.update(pm[0].id, pm_update)

    async def delete_project_member(
        self, filters: ProjectMembersFilters
    ) -> Optional[ProjectMemberPublic]:
        pm = await self.__project_member_repository.fetch(filters)

        if len(pm) == 0:
            return None

        return await self.__project_member_repository.delete(pm[0].id)
