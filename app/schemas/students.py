from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import field_validator

from app.models.students import SlotType
from app.schemas.base import CommonListFilters


class StudentFilters(CommonListFilters):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('sort_by')
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['email', 'first_name', 'last_name', 'registred_at']

        if v not in allowed_filters:
            raise ValueError(
                f"Student sorting by '{v}' not allowed. Allowed: {allowed_filters}"
            )
        return v


class BusySlotFilters(CommonListFilters):
    slot_type: Optional[SlotType] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    student_id: Optional[UUID] = None

    @field_validator('sort_by')
    def validate_sort_field(self, v):
        if v is None:
            return v

        allowed_filters = ['slot_type', 'start_datetime', 'end_datetime', 'created_at']

        if v not in allowed_filters:
            raise ValueError(
                f"BusySlot sorting by '{v}' not allowed. Allowed: {allowed_filters}"
            )
        return v
