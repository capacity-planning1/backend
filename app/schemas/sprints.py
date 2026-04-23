from datetime import date, datetime
from typing import Optional
from uuid import UUID

from app.models.sprints import (
    StatusType,
    TaskChangeRequestStatus,
    TaskPriority,
)
from app.schemas.base import CommonListFilters


class SprintFilters(CommonListFilters):
    name: Optional[str] = None
    project_id: Optional[UUID] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: Optional[datetime] = None
    _allowed_sort_fields = ['name', 'start_date', 'end_date', 'created_at']


class SprintTaskFilters(CommonListFilters):
    title: Optional[str] = None
    status: Optional[StatusType] = None
    priority: Optional[TaskPriority] = None
    created_at: Optional[datetime] = None
    project_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    _allowed_sort_fields = ['title', 'status', 'priority', 'created_at']


class TaskAssignmentFilters(CommonListFilters):
    project_member_id: Optional[UUID] = None
    project_task_id: Optional[UUID] = None
    assignet_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    _allowed_sort_fields = ['assignet_at', 'accepted_at']


class TaskChangeRequestFilters(CommonListFilters):
    status: Optional[TaskChangeRequestStatus] = None
    requested_by_member_id: Optional[UUID] = None
    task_assignment_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    handled_at: Optional[datetime] = None
    _allowed_sort_fields = ['name', 'created_at']
