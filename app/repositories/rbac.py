from typing import Optional, List
from uuid import UUID

from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.rbac import RoleModel, PermissionModel, UserRoleLink, RolePermissionLink
from app.utils.repository import Repository


class RoleRepository(Repository[RoleModel]):
    async def get_by_code(self, code: str) -> Optional[RoleModel]:
        """Получить роль по коду"""
        select_statement = select(RoleModel).where(RoleModel.code == code)
        result = await self._session.execute(select_statement)
        return result.scalar_one_or_none()

    async def get_all_roles(self, skip: int = 0, limit: int = 100) -> List[RoleModel]:
        """Получить все роли"""
        select_statement = select(RoleModel).offset(skip).limit(limit)
        result = await self._session.execute(select_statement)
        return list(result.scalars().all())

    async def delete_role(self, role_id: UUID) -> bool:
        """Удалить роль (только если не системная)"""
        role = await self.get(role_id)
        if not role or role.is_system:
            return False
        await self._session.delete(role)
        await self._session.commit()
        return True


class PermissionRepository(Repository[PermissionModel]):
    async def get_by_code(self, code: str) -> Optional[PermissionModel]:
        """Получить разрешение по коду"""
        select_statement = select(PermissionModel).where(PermissionModel.code == code)
        result = await self._session.execute(select_statement)
        return result.scalar_one_or_none()

    async def get_or_create(self, name: str, code: str, description: str = None) -> PermissionModel:
        """Получить или создать разрешение"""
        permission = await self.get_by_code(code)
        if not permission:
            permission = PermissionModel(
                name=name,
                code=code,
                description=description
            )
            permission = await self.save(permission)
        return permission

    async def get_all_permissions(self) -> List[PermissionModel]:
        """Получить все разрешения"""
        select_statement = select(PermissionModel)
        result = await self._session.execute(select_statement)
        return list(result.scalars().all())


class UserRoleRepository(Repository[UserRoleLink]):
    async def assign_role(self, student_id: UUID, role_id: UUID) -> bool:
        """Назначить роль пользователю"""
        select_statement = select(UserRoleLink).where(
            and_(
                UserRoleLink.student_id == student_id,
                UserRoleLink.role_id == role_id
            )
        )
        result = await self._session.execute(select_statement)
        if result.scalar_one_or_none():
            return False

        link = UserRoleLink(student_id=student_id, role_id=role_id)
        self._session.add(link)
        await self._session.commit()
        return True

    async def remove_role(self, student_id: UUID, role_id: UUID) -> bool:
        """Удалить роль у пользователя"""
        select_statement = select(UserRoleLink).where(
            and_(
                UserRoleLink.student_id == student_id,
                UserRoleLink.role_id == role_id
            )
        )
        result = await self._session.execute(select_statement)
        link = result.scalar_one_or_none()

        if not link:
            return False

        await self._session.delete(link)
        await self._session.commit()
        return True

    async def get_user_roles(self, student_id: UUID) -> List[RoleModel]:
        """Получить все роли пользователя"""
        select_statement = (
            select(RoleModel)
            .join(UserRoleLink, RoleModel.id == UserRoleLink.role_id)
            .where(UserRoleLink.student_id == student_id)
        )
        result = await self._session.execute(select_statement)
        return list(result.scalars().all())

    async def get_user_permission_codes(self, student_id: UUID) -> List[str]:
        """Получить все permission коды пользователя через его роли"""
        select_statement = (
            select(PermissionModel.code)
            .select_from(UserRoleLink)
            .join(RoleModel, RoleModel.id == UserRoleLink.role_id)
            .join(RolePermissionLink, RolePermissionLink.role_id == RoleModel.id)
            .join(PermissionModel, PermissionModel.id == RolePermissionLink.permission_id)
            .where(UserRoleLink.student_id == student_id)
            .distinct()
        )
        result = await self._session.execute(select_statement)
        return list(result.scalars().all())
