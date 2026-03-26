from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import field_validator

from app.schemas.base import CommonListFilters


class ProjectFilters(CommonListFilters):
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    owner_student_id: Optional[UUID] = None

    @field_validator('sort_by')
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['name', 'created_at']

        if v not in allowed_filters:
            raise ValueError(
                f"Project sorting by '{v}' not allowed. Allowed: {allowed_filters}"
            )
        return v


class ProjectMembersFilters(CommonListFilters):
    project_id: Optional[UUID] = None
    student_id: Optional[UUID] = None
    role: Optional[str] = None
    join_date: Optional[date] = None
    is_active: Optional[bool] = None

    @field_validator('sort_by')
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['role', 'join_date', 'is_active']

        if v not in allowed_filters:
            raise ValueError(
                f"ProjectMember sorting by '{v}' not allowed. "
                f'Allowed: {allowed_filters}'
            )
        return v


class TeamFilters(CommonListFilters):
    name: Optional[str] = None
    project_id: Optional[UUID] = None

    @field_validator('sort_by')
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['name']

        if v not in allowed_filters:
            raise ValueError(
                f"Team sorting by '{v}' not allowed. Allowed: {allowed_filters}"
            )
        return v


class TeamMembershipFilters(CommonListFilters):
    team_id: Optional[UUID] = None
    project_member_id: Optional[UUID] = None

    @field_validator('sort_by')
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['position']

        if v not in allowed_filters:
            raise ValueError(
                f"TeamMembership sorting by '{v}' not allowed. "
                f'Allowed: {allowed_filters}'
            )
        return v
