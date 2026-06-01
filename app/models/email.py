from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import Field

from app.core.config import settings
from app.models.base import BaseModel


class EmailAction(str, Enum):
    VERIFY_EMAIL = 'verify email'
    CHANGE_PASSWORD = 'change password'


class EmailStatus(str, Enum):
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'


class EmailNotification(BaseModel, table=True):
    __tablename__ = 'email_notification'

    student_id: UUID = Field(foreign_key='student.id', nullable=False)
    action: EmailAction = Field(nullable=False)
    expires_at: datetime = Field(default_factory=lambda: (
            datetime.now(timezone.utc)
            + timedelta(seconds=settings.email.notification_lifetime_seconds)
        ))
    status: EmailStatus = Field(default=EmailStatus.PENDING, nullable=False)
    code: UUID = Field(default_factory=uuid4)
    is_used: bool = Field(default=False, nullable=False)
