from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status

from app.core.auth import create_token, decode_token
from app.core.config import settings
from app.dependencies.auth import authenticate_student
from app.dependencies.repositories import StudentSessionRepositoryDep
from app.dependencies.services import StudentServiceDep
from app.models.auth.refresh_session import (
    StudentSessionModel,
    StudentSessionUpdate,
)
from app.schemas.auth import StudentSessionFilters


class StudentSessionService:
    def __init__(self, refresh_session_repo: StudentSessionRepositoryDep):
        self.__repo = refresh_session_repo

    async def login(
        self,
        email: str,
        password: str,
        user_agent: str,
        student_service: StudentServiceDep,
    ):
        student = await authenticate_student(email, password, student_service)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User with this email already exists',
            )

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
        return await self.__repo.save(refresh_session)

    async def validate_session(self, refresh_token: str) -> Optional[tuple[UUID, str]]:
        payload = decode_token(refresh_token)
        if not payload:
            return None

        jti = payload.get('jti')
        student_id_str = payload.get('sub')

        if not jti or not student_id_str:
            return None

        filters = StudentSessionFilters()
        filters.jti = jti
        filters.is_revoked = False

        sessions = await self.__repo.fetch(filters)
        active_sessions = [
            s for s in sessions.items if s.expires_at > datetime.now(timezone.utc)
        ]

        if len(active_sessions) == 0:
            return None

        return (UUID(student_id_str), jti)

    async def revoke_session(self, jti: str) -> bool:
        filters = StudentSessionFilters()
        filters.jti = jti
        return (
            await self.__repo.update_by_filters(
                StudentSessionUpdate(is_revoked=True), filters
            )
            > 0
        )

    async def revoke_all_student_sessions(self, student_id: UUID) -> int:
        filters = StudentSessionFilters()
        filters.student_id = student_id
        return await self.__repo.update_by_filters(
            StudentSessionUpdate(is_revoked=True), filters
        )

    async def refresh_tokens(
        self, old_refresh_token: str, user_agent: str | None = None
    ) -> tuple[str, str, str] | None:
        result = await self.validate_session(old_refresh_token)
        if not result:
            return None

        student_id, old_jti = result

        await self.revoke_session(old_jti)

        new_access_token = create_token(
            student_id, settings.auth.access_token_lifetime_seconds
        )
        new_refresh_token = create_token(
            student_id, settings.auth.refresh_token_lifetime_seconds
        )

        new_payload = decode_token(new_refresh_token)
        if not new_payload:
            return None

        new_jti = new_payload.get('jti')
        exp_timestamp = new_payload.get('exp')
        if exp_timestamp is not None:
            new_exp = datetime.fromtimestamp(float(exp_timestamp), tz=timezone.utc)
        else:
            return None

        session = StudentSessionModel(
            jti=new_jti,
            student_id=student_id,
            expires_at=new_exp,
            user_agent=user_agent,
        )

        await self.__repo.save(session)

        return (new_access_token, new_refresh_token, str(student_id))
