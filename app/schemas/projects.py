from datetime import date, datetime
from typing import Optional
from uuid import UUID

from app.schemas.base import CommonListFilters


class ProjectFilters(CommonListFilters):
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    owner_student_id: Optional[UUID] = None
    _allowed_sort_fields = ['name', 'created_at']


class ProjectMembersFilters(CommonListFilters):
    project_id: Optional[UUID] = None
    student_id: Optional[UUID] = None
    role: Optional[str] = None
    join_date: Optional[date] = None
    is_active: Optional[bool] = None
    _allowed_sort_fields = ['role', 'join_date', 'is_active']


class TeamFilters(CommonListFilters):
    name: Optional[str] = None
    project_id: Optional[UUID] = None
    _allowed_sort_fields = ['name']


class TeamMembershipFilters(CommonListFilters):
    team_id: Optional[UUID] = None
    project_member_id: Optional[UUID] = None
    _allowed_sort_fields = ['position']
