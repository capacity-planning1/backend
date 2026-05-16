from typing import List, Sequence, Set
from uuid import UUID

from app.models.rbac import RoleModel

from app.dependencies.repositories import (
    PermissionRepository,
    PermissionRepositoryDep,
    RoleRepository,
    RoleRepositoryDep,
    StudentRepository,
    StudentRepositoryDep,
)
from app.schemas.rbac import (
    PermissionFilters,
    RoleFilters,
)


class RoleService:
    __student_repo: StudentRepository
    __role_repo: RoleRepository
    __permission_repo: PermissionRepository

    def __init__(
        self,
        student_repo: StudentRepositoryDep,
        role_repo: RoleRepositoryDep,
        permission_repo: PermissionRepositoryDep,
    ):
        self.__student_repo = student_repo
        self.__role_repo = role_repo
        self.__permission_repo = permission_repo

    async def get_role_by_code(self, code: str) -> RoleModel | None:
        filters = RoleFilters(code=code)
        roles = await self.__role_repo.fetch(filters)
        if len(roles) == 0:
            return None
        return roles[0]

    async def get_role_by_id(self, role_id: UUID) -> RoleModel | None:
        return await self.__role_repo.get(role_id)

    async def get_all_roles(self) -> Sequence[RoleModel]:
        return await self.__role_repo.fetch()

    async def get_user_permissions(self, student_id: UUID) -> Set[str]:
        student = await self.__student_repo.get(student_id)
        if not student:
            return set[str]()

        permissions = set[str]()
        for role in student.roles:
            permissions.update(permission.code for permission in role.permissions)

        return permissions

    async def assign_role_to_user(self, student_id: UUID, role_code: str) -> bool:
        filters = RoleFilters(code=role_code)
        roles = await self.__role_repo.fetch(filters)
        if len(roles) == 0:
            return False

        student = await self.__student_repo.get(student_id)
        if not student:
            return False

        if roles[0] in student.roles:
            return False

        student.roles.append(roles[0])
        await self.__student_repo.save(student)
        return True

    async def remove_role_from_user(self, student_id: UUID, role_code: str) -> bool:
        filters = RoleFilters(code=role_code)
        roles = await self.__role_repo.fetch(filters)
        if len(roles) == 0:
            return False

        student = await self.__student_repo.get(student_id)
        if not student:
            return False
        if roles[0] not in student.roles:
            return False
        student.roles.remove(roles[0])
        await self.__student_repo.save(student)
        return True

    async def get_user_roles(self, student_id: UUID) -> Sequence[RoleModel] | None:
        student = await self.__student_repo.get(student_id)
        if not student:
            return None
        return student.roles

    async def create_role(
        self,
        name: str,
        code: str,
        description: str | None = None,
        permission_codes: List[str] | None = None,
    ) -> RoleModel:
        role = RoleModel(name=name, code=code, description=description, is_system=False)
        role = await self.__role_repo.save(role)

        if permission_codes:
            for perm_code in permission_codes:
                filters = PermissionFilters(code=perm_code)
                permissions = await self.__permission_repo.fetch(filters)
                if len(permissions) != 0:
                    role.permissions.append(permissions[0])
            role = await self.__role_repo.save(role)

        return role
