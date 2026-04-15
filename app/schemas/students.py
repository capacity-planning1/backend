from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.students import SlotType
from app.schemas.base import CommonListFilters


class StudentFilters(CommonListFilters):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    _allowed_sort_fields = ['email', 'first_name', 'last_name', 'registred_at']


class BusySlotFilters(CommonListFilters):
    slot_type: Optional[SlotType] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    student_id: Optional[UUID] = None
    _allowed_sort_fields = ['slot_type', 'start_datetime', 'end_datetime', 'created_at']
