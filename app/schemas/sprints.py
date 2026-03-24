from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import field_validator

from app.models.sprints import (
    StatusType,
    TaskChangeRequestStatus,
    TaskPriority,
)
from app.schemas.base import CommonListFilters


class SptintFilters(CommonListFilters):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: Optional[datetime] = None

    @field_validator("sort_by")
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['name', 'start_date', 'end_date', 'created_at']

        if v not in allowed_filters:
            raise ValueError(
                f"Project sorting by '{v}' not allowed. "
                f"Allowed: {allowed_filters}"
            )
        return v


class SprintTaskFilters(CommonListFilters):
    title: Optional[str] = None
    status: Optional[StatusType] = None
    priority: Optional[TaskPriority] = None
    created_at: Optional[datetime] = None

    @field_validator("sort_by")
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['title', 'status', 'priority', 'created_at']

        if v not in allowed_filters:
            raise ValueError(
                f"Project sorting by '{v}' not allowed. "
                f"Allowed: {allowed_filters}"
            )
        return v


class TaskAssignmentFilters(CommonListFilters):
    project_member: Optional[UUID] = None
    assignet_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None

    @field_validator("sort_by")
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['assignet_at', 'accepted_at']

        if v not in allowed_filters:
            raise ValueError(
                f"Project sorting by '{v}' not allowed. "
                f"Allowed: {allowed_filters}"
            )
        return v


class TaskChangeRequestFilters(CommonListFilters):
    status: Optional[TaskChangeRequestStatus] = None
    requested_by_member_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    handled_at: Optional[datetime] = None

    @field_validator("sort_by")
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['name', 'created_at']

        if v not in allowed_filters:
            raise ValueError(
                f"Project sorting by '{v}' not allowed. "
                f"Allowed: {allowed_filters}"
            )
        return v
