from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.core.auth import decode_token, create_refresh_token, create_access_token
from app.dependencies.repositories import RefreshSessionRepositoryDep
from app.models.auth.refresh_session import (
    RefreshSessionUpdate,
    RefreshSessionModel,
)    
from app.schemas.auth import RefreshSessionFilters


class RefreshSessionService:
    def __init__(self, refresh_session_repo: RefreshSessionRepositoryDep):
        self.__repo = refresh_session_repo

    async def create_session(self, refresh_session: RefreshSessionModel):
        return await self.__repo.save(refresh_session)

    async def validate_session(self, refresh_token: str) -> Optional[tuple[UUID, str]]:
        payload = decode_token(refresh_token)
        if not payload:
            return None

        jti = payload.get("jti")
        student_id_str = payload.get("sub")

        if not jti or not student_id_str:
            return None

        filters = RefreshSessionFilters()
        filters.jti = jti
        filters.is_revoked = False

        sessions = await self.__repo.fetch(filters)
        active_sessions = [s for s in sessions
            if s.expires_at > datetime.now(timezone.utc)
        ]

        if len(active_sessions) == 0:
            return None

        return (UUID(student_id_str), jti)

    async def revoke_session(self, jti: str) -> bool:
        filters = RefreshSessionFilters()
        filters.jti = jti
        return await self.__repo.update_by_filters(
            RefreshSessionUpdate(is_revoked=True), filters)

    async def revoke_all_student_sessions(self, student_id: UUID) -> int:
        filters = RefreshSessionFilters()
        filters.student_id = student_id
        return await self.__repo.update_by_filters(
            RefreshSessionUpdate(is_revoked=True), filters)

    async def refresh_tokens(self, old_refresh_token: str,
        user_agent: str | None = None, 
        ip_address: str | None = None) -> tuple[str, str, str] | None:
        result = await self.validate_session(old_refresh_token)
        if not result:
            return None

        student_id, old_jti = result

        await self.revoke_session(old_jti)

        new_access_token = create_access_token(student_id)
        new_refresh_token = create_refresh_token(student_id)

        new_payload = decode_token(new_refresh_token)
        if not new_payload:
            return None

        new_jti = new_payload.get("jti")
        exp_timestamp = new_payload.get("exp")
        if exp_timestamp is not None:
            new_exp = datetime.fromtimestamp(float(exp_timestamp), tz=timezone.utc)
        else:
            return None

        session = RefreshSessionModel(
            jti=new_jti,
            student_id=student_id,
            expires_at=new_exp,
            user_agent=user_agent,
            ip_address=ip_address
        )

        await self.__repo.save(session)

        return (new_access_token, new_refresh_token, str(student_id))
