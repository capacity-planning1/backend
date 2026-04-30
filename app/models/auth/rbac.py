from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.students.student import StudentModel


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link"

    student_id: UUID = Field(foreign_key="student.id", primary_key=True)
    role_id: UUID = Field(foreign_key="role.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = "role_permission_link"

    role_id: UUID = Field(foreign_key="role.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="permission.id", primary_key=True)


class PermissionModel(BaseModel, table=True):
    __tablename__ = "permission"

    name: str = Field(unique=True, nullable=False, max_length=255)
    code: str = Field(unique=True, nullable=False, max_length=255, index=True)
    description: str | None = Field(default=None, max_length=500)

    roles: List["RoleModel"] = Relationship(
        back_populates="permissions",
        link_model=RolePermissionLink
    )


class RoleModel(BaseModel, table=True):
    __tablename__ = "role"

    name: str = Field(unique=True, nullable=False, max_length=100)
    code: str = Field(unique=True, nullable=False, max_length=100, index=True)
    description: str | None = Field(default=None, max_length=500)
    is_system: bool = Field(default=False, nullable=False)

    users: List["StudentModel"] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink
    )
    permissions: List[PermissionModel] = Relationship(
        back_populates="roles",
        link_model=RolePermissionLink
    )
