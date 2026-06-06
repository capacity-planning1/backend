from typing import Optional
from uuid import UUID

from app.models.email import EmailAction, EmailStatus
from app.schemas.base import CommonListFilters


class EmailNotificationFilters(CommonListFilters):
    code: Optional[UUID] = None
    action: Optional[EmailAction] = None
    status: Optional[EmailStatus] = None
    student_id: Optional[UUID] = None
