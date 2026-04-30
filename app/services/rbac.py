from typing import List, Set
from uuid import UUID

from app.dependencies.repositories import (
    RoleRepositoryDep,
    PermissionRepositoryDep,
    UserRoleRepositoryDep
)

from app.models.rbac import RoleModel


class RoleService:
    def __init__(
        self,
        role_repo: RoleRepositoryDep,
        permission_repo: PermissionRepositoryDep,
        user_role_repo: UserRoleRepositoryDep
    ):
        self._role_repo = role_repo
        self._permission_repo = permission_repo
        self._user_role_repo = user_role_repo

    async def get_role_by_code(self, code: str) -> RoleModel | None:
        return await self._role_repo.get_by_code(code)

    async def get_role_by_id(self, role_id: UUID) -> RoleModel | None:
        return await self._role_repo.get(role_id)

    async def get_all_roles(self) -> List[RoleModel]:
        return await self._role_repo.get_all_roles()

    async def get_user_permissions(self, student_id: UUID) -> Set[str]:
        permission_codes = await self._user_role_repo.get_user_permission_codes(student_id)
        return set(permission_codes)

    async def assign_role_to_user(self, student_id: UUID, role_code: str) -> bool:
        role = await self._role_repo.get_by_code(role_code)
        if not role:
            return False
        return await self._user_role_repo.assign_role(student_id, role.id)

    async def remove_role_from_user(self, student_id: UUID, role_code: str) -> bool:
        role = await self._role_repo.get_by_code(role_code)
        if not role:
            return False

        if role_code == "user":
            return False
        return await self._user_role_repo.remove_role(student_id, role.id)

    async def get_user_roles(self, student_id: UUID) -> List[RoleModel]:
        return await self._user_role_repo.get_user_roles(student_id)

    async def create_role(
        self,
        name: str,
        code: str,
        description: str | None = None,
        permission_codes: List[str] | None = None
    ) -> RoleModel:
        role = RoleModel(
            name=name,
            code=code,
            description=description,
            is_system=False
        )
        role = await self._role_repo.save(role)

        if permission_codes:
            for perm_code in permission_codes:
                permission = await self._permission_repo.get_by_code(perm_code)
                if permission:
                    role.permissions.append(permission)
            role = await self._role_repo.save(role)

        return role
