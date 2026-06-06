from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from app.core.config import settings
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.students.student import StudentModel


class EmailAction(str, Enum):
    VERIFY_EMAIL = 'verify email'
    CHANGE_PASSWORD = 'change password'


class EmailStatus(str, Enum):
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'


class EmailNotification(BaseModel, table=True):
    __tablename__ = 'email_notification'

    student_id: UUID = Field(foreign_key='student.id', nullable=False, index=True)
    student: 'StudentModel' = Relationship(
        sa_relationship=relationship(
            'StudentModel',
            back_populates='email_notifications',
            lazy='selectin',
        )
    )
    action: EmailAction = Field(nullable=False)
    expires_at: datetime = Field(
        default_factory=lambda: (
            datetime.now(timezone.utc)
            + timedelta(seconds=settings.email.notification_lifetime_seconds)
        ),
        sa_type=DateTime(timezone=True),
    )
    status: EmailStatus = Field(default=EmailStatus.PENDING, nullable=False)
    code: UUID = Field(default_factory=uuid4)
    is_used: bool = Field(default=False, nullable=False)
