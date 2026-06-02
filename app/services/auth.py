from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import BackgroundTasks

from app.core.auth import create_token, decode_token
from app.core.config import settings
from app.dependencies.auth import authenticate_student
from app.dependencies.repositories import (
    EmailNotificationRepositoryDep,
    StudentRepositoryDep,
    StudentSessionRepositoryDep,
)
from app.models.auth.refresh_session import (
    StudentSessionModel,
    StudentSessionUpdate,
)
from app.models.email import EmailAction, EmailNotification
from app.models.students.student import StudentCreate, StudentModel
from app.schemas.auth import AuthFilters
from app.schemas.email import EmailNotificationFilters
from app.schemas.students import StudentFilters
from app.services.email import EmailService
from app.utils.errors import (
    BadRequestError,
    ConflictError,
    GoneError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
)
from app.utils.hasher import Hasher


class AuthService:
    def __init__(
        self,
        refresh_session_repo: StudentSessionRepositoryDep,
        email_notification_repo: EmailNotificationRepositoryDep,
        student_repo: StudentRepositoryDep,
        background_tasks: BackgroundTasks
    ):
        self.__refresh_session_repo = refresh_session_repo
        self.__email_notification_repo = email_notification_repo
        self.__student_repo = student_repo
        self.__email_service = EmailService(background_tasks=background_tasks)

    async def register(
        self, student_create: StudentCreate
    ) -> None:
        filters = StudentFilters(email=student_create.email)
        existing = await self.__student_repo.fetch(filters=filters)

        if len(existing) != 0:
            raise ConflictError(message='User with this email is already exists')

        student_dump = student_create.model_dump()
        student_dump['hashed_password'] = Hasher.get_password_hash(
            student_dump.pop('password')
        )
        student = StudentModel(**student_dump)

        created_student = await self.__student_repo.save(student)
        notification = await self.__email_notification_repo.save(
            EmailNotification(
                student_id=created_student.id,
                action=EmailAction.VERIFY)
        )

        self.__email_service.send_verification_email(
            email_to=created_student.email,
            verification_code=notification.code,
            verification_link=self._build_verify_account_url(
                created_student.id, notification.code)
        )

    async def login(
        self,
        email: str,
        password: str,
        user_agent: str,
        student_repo: StudentRepositoryDep,
    ):
        student = await authenticate_student(email, password, student_repo)

        if student is None:
            raise UnauthorizedError('Wrong email or password')

        access_token = create_token(
            student.id, settings.auth.access_token_lifetime_seconds
        )
        refresh_token = create_token(
            student.id, settings.auth.refresh_token_lifetime_seconds
        )

        refresh_payload = decode_token(refresh_token)

        self.create_session(
            jti=refresh_payload.get('jti'),
            student_id=student.id,
            expires_at=datetime.fromtimestamp(
                float(refresh_payload['exp']), tz=timezone.utc
            ),
            user_agent=user_agent,
        )

        return (access_token, refresh_token)

    async def create_session(self, refresh_session: StudentSessionModel):
        return await self.__refresh_session_repo.save(refresh_session)

    async def validate_session(self, refresh_token: str) -> Optional[tuple[UUID, str]]:
        payload = decode_token(refresh_token)
        if not payload:
            raise UnauthorizedError()

        jti = payload.get('jti')
        student_id_str = payload.get('sub')

        if not jti or not student_id_str:
            return UnauthorizedError()

        filters = AuthFilters()
        filters.jti = jti
        filters.is_revoked = False

        sessions = await self.__refresh_session_repo.fetch(filters)
        active_sessions = [
            s for s in sessions.items if s.expires_at > datetime.now(timezone.utc)
        ]

        if len(active_sessions) == 0:
            return UnauthorizedError()

        return (UUID(student_id_str), jti)

    async def revoke_session(self, jti: str) -> bool:
        filters = AuthFilters()
        filters.jti = jti
        return (
            await self.__refresh_session_repo.update_by_filters(
                StudentSessionUpdate(is_revoked=True), filters
            )
            > 0
        )

    async def revoke_all_student_sessions(self, student_id: UUID) -> int:
        filters = AuthFilters()
        filters.student_id = student_id
        return await self.__refresh_session_repo.update_by_filters(
            StudentSessionUpdate(is_revoked=True), filters
        )

    async def refresh_tokens(
        self, old_refresh_token: str, user_agent: str | None = None
    ) -> tuple[str, str, str] | None:
        student_id, old_jti = await self.validate_session(old_refresh_token)

        await self.revoke_session(old_jti)

        new_access_token = create_token(
            student_id, settings.auth.access_token_lifetime_seconds
        )
        new_refresh_token = create_token(
            student_id, settings.auth.refresh_token_lifetime_seconds
        )

        new_payload = decode_token(new_refresh_token)
        if not new_payload:
            raise InternalServerError()

        new_jti = new_payload.get('jti')
        exp_timestamp = new_payload.get('exp')
        if exp_timestamp is not None:
            new_exp = datetime.fromtimestamp(float(exp_timestamp), tz=timezone.utc)
        else:
            raise InternalServerError()

        session = StudentSessionModel(
            jti=new_jti,
            student_id=student_id,
            expires_at=new_exp,
            user_agent=user_agent,
        )

        await self.__refresh_session_repo.save(session)

        return (new_access_token, new_refresh_token, str(student_id))

    async def verify_email(self, student_id: UUID, code: UUID) -> None:
        student = await self.__student_repo.get(student_id)
        if student is None:
            raise NotFoundError('Student not found')

        filters = EmailNotificationFilters(
            code=code,
            student_id=student_id,
            action=EmailAction.VERIFY)
        notifications = await self.__email_notification_repo.fetch(filters)

        if len(notifications) == 0:
            raise NotFoundError("No such request exists")

        notification = notifications[0]
        if (notification.expires_at < datetime.now(timezone.utc)
                or notification.is_used):
            raise GoneError("The code has expired")

        notification.is_used = True

        student.is_email_verificated = True
        await self.__student_repo.save(student)

    async def send_change_password_code(self, student_id: UUID) -> None:
        student = await self.__student_repo.get(student_id)
        if student is None:
            raise NotFoundError('User not found')

        notification = await self.__email_notification_repo.save(
            EmailNotification(
                student_id=student_id,
                action=EmailAction.CHANGE_PASSWORD)
        )

        self.__email_service.send_change_password_email(
            email_to=student.email,
            reset_code=notification.code,
            reset_link=self._build_change_password_url(student_id, notification.code)
        )

    async def confirm_change_password(
        self,
        student_id: UUID,
        code: UUID,
        new_password: str,
        repeat_password: str
    ) -> None:
        if new_password != repeat_password:
            raise BadRequestError("Passwords don't match")

        student = await self.__student_repo.get(student_id)
        if student is None:
            raise NotFoundError("User not found")

        filters = EmailNotificationFilters(
            student_id=student_id,
            code=code,
            action=EmailAction.CHANGE_PASSWORD)
        notifications = await self.__email_notification_repo.fetch(filters)

        if len(notifications) == 0:
            raise NotFoundError("No such request exists")

        notification = notifications[0]
        if (notification.expires_at < datetime.now(timezone.utc)
                or notification.is_used):
            raise GoneError("The code has expired")

        notification.is_used = True
        student.hashed_password = Hasher.get_password_hash(new_password)
        await self.__student_repo.save(student)

    def _build_verify_account_url(self, student_id: UUID, code: UUID) -> str:
        return (
            f'{settings.common.frontend_host}'
            f'/verify-account?student_id={student_id}&code={code}'
        )

    def _build_change_password_url(self, student_id: UUID, code: UUID) -> str:
        return (
            f'{settings.common.frontend_host}'
            f'/reset-password?student_id={student_id}&code={code}'
        )
