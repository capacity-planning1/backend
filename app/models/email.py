from datetime import datetime, timezone, timedelta
from uuid import UUID
from enum import Enum

from sqlmodel import Field

from app.core.config import settings
from app.models.base import BaseModel


class EmailAction(int, Enum):
    VERIFY = 0
    CHANGE_PASSWORD = 1


class EmailNotification(BaseModel, table=True):
    __tablename__ = 'email_notification'

    student_id: UUID = Field(foreign_key='student.id', nullable=False)
    action: EmailAction = Field(nullable=False)
    expires_at: datetime = Field(default_factory=lambda: (
            datetime.now(timezone.utc)
            + timedelta(seconds=settings.email.notification_lifetime_seconds)
        ))
    is_used: bool = Field(default=False, nullable=False)
