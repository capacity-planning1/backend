from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    ProjectMemberRepository,
    ProjectMemberRepositoryDep,
    ProjectRepository,
    ProjectRepositoryDep,
    TeamMembershipRepository,
    TeamMembershipRepositoryDep,
    TeamRepository,
    TeamRepositoryDep,
)
from app.models.projects import (
    ProjectCreate,
    ProjectMemberCreate,
    ProjectMemberModel,
    ProjectMemberPublic,
    ProjectMemberUpdate,
    ProjectModel,
    ProjectUpdate,
    TeamCreate,
    TeamMembershipCreate,
    TeamMembershipModel,
    TeamMembershipPublic,
    TeamMembershipUpdate,
    TeamModel,
    TeamPublic,
    TeamUpdate,
)
from app.schemas.projects import (
    ProjectFilters,
    ProjectMembersFilters,
    TeamFilters,
    TeamMembershipFilters,
)


class ProjectService:
    __project_repository: ProjectRepository

    def __init__(
        self,
        project_repository: ProjectRepositoryDep,
    ):
        self.__project_repository = project_repository

    async def get_projects(self, filters: ProjectFilters) -> Sequence[ProjectModel]:
        return await self.__project_repository.fetch(filters)

    async def create_project(self, project_create: ProjectCreate) -> ProjectModel:
        project_dump = project_create.model_dump()
        project = ProjectModel(**project_dump)
        return await self.__project_repository.save(project)

    async def get_project(self, project_id: UUID) -> Optional[ProjectModel]:
        return await self.__project_repository.get(project_id)

    async def update_project(
        self, project_update: ProjectUpdate, project_id: UUID
    ) -> Optional[ProjectModel]:
        return await self.__project_repository.update(project_id, project_update)

    async def delete_project(self, project_id: UUID) -> Optional[ProjectModel]:
        return await self.__project_repository.delete(project_id)


class ProjectMemberService:
    __project_member_repository: ProjectMemberRepository

    def __init__(
        self,
        project_repository: ProjectRepositoryDep,
        project_member_repository: ProjectMemberRepositoryDep,
    ):
        self.__project_repository = project_repository
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
        self, student_id: UUID, project_id: UUID
    ) -> Optional[ProjectMemberPublic]:
        filters = ProjectMembersFilters()
        filters.student_id = student_id
        filters.project_id = project_id
        result = await self.__project_member_repository.fetch(filters)

        if result is None:
            return None

        return result[0]

    async def update_project_member(
        self, project_id: UUID, student_id: UUID, pm_update: ProjectMemberUpdate
    ) -> Optional[ProjectMemberPublic]:
        filters = ProjectMembersFilters()
        filters.project_id = project_id
        filters.student_id = student_id

        pm = await self.__project_member_repository.fetch(filters)

        if pm is None:
            return None

        return await self.__project_member_repository.update(pm[0].id, pm_update)

    async def delete_project_member(
        self, project_id: UUID, student_id: UUID
    ) -> Optional[ProjectMemberPublic]:
        filters = ProjectMembersFilters()
        filters.project_id = project_id
        filters.student_id = student_id

        pm = await self.__project_member_repository.fetch(filters)

        if pm is None:
            return None

        return await self.__project_member_repository.delete(pm[0].id)


class TeamService:
    __team_repository: TeamRepository

    def __init__(self, team_repository: TeamRepositoryDep):
        self.__team_repository = team_repository

    async def get_teams(self, filters: TeamFilters) -> Sequence[TeamPublic]:
        return await self.__team_repository.fetch(filters)

    async def create_team(self, team_create: TeamCreate) -> TeamPublic:
        team_dump = team_create.model_dump()
        team = TeamModel(**team_dump)
        return await self.__team_repository.save(team)

    async def get_team(self, team_id: UUID) -> Optional[TeamPublic]:
        return await self.__team_repository.get(team_id)

    async def update_team(
        self, team_id: UUID, team_update: TeamUpdate
    ) -> Optional[TeamPublic]:
        return await self.__team_repository.update(team_id, team_update)

    async def delete_team(self, team_id: UUID) -> Optional[TeamPublic]:
        return await self.__team_repository.delete(team_id)


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
        self, team_id: UUID, pm_id: UUID
    ) -> Optional[TeamMembershipPublic]:
        filters = TeamMembershipFilters()
        filters.team_id = team_id
        filters.project_member_id = pm_id
        result = await self.__team_membership_repository.fetch(filters)

        if result is None:
            return None
        return result[0]

    async def update_membership(
        self, team_id: UUID, pm_id: UUID, tm_update: TeamMembershipUpdate
    ) -> Optional[TeamMembershipPublic]:
        filters = TeamMembershipFilters()
        filters.team_id = team_id
        filters.project_member_id = pm_id

        tm = await self.__team_membership_repository.fetch(filters)

        if tm is None:
            return None

        return await self.__team_membership_repository.update(tm[0].id, tm_update)

    async def delete_membership(
        self, team_id: UUID, pm_id: UUID
    ) -> Optional[TeamMembershipPublic]:
        filters = TeamMembershipFilters()
        filters.team_id = team_id
        filters.project_member_id = pm_id

        tm = await self.__team_membership_repository.fetch(filters)

        if tm is None:
            return None

        return await self.__team_membership_repository.delete(tm[0].id)
