from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.core.auth import decode_token, create_refresh_token, create_access_token
from app.dependencies.repositories import RefreshSessionRepositoryDep


class RefreshSessionService:
    def __init__(self, refresh_session_repo: RefreshSessionRepositoryDep):
        self._repo = refresh_session_repo

    async def create_session(self, jti: str, student_id: UUID, expires_at: datetime,
        user_agent: str | None = None, ip_address: str | None = None):
        return await self._repo.create(jti, student_id, expires_at, user_agent, ip_address)

    async def validate_session(self, refresh_token: str) -> Optional[tuple[UUID, str]]:
        payload = decode_token(refresh_token)
        if not payload:
            return None

        jti = payload.get("jti")
        student_id_str = payload.get("sub")

        if not jti or not student_id_str:
            return None

        session = await self._repo.get_active_by_jti(jti)
        if not session:
            return None

        return (UUID(student_id_str), jti)

    async def revoke_session(self, jti: str) -> bool:
        return await self._repo.revoke_session(jti)

    async def revoke_all_student_sessions(self, student_id: UUID) -> int:
        return await self._repo.revoke_all_student_sessions(student_id)

    async def refresh_tokens(self, old_refresh_token: str,
        user_agent: str | None = None, 
        ip_address: str | None = None) -> tuple[str, str, str] | None:
        result = await self.validate_session(old_refresh_token)
        if not result:
            return None

        student_id, old_jti = result

        await self._repo.revoke_session(old_jti)

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

        await self._repo.create(new_jti, student_id, new_exp, user_agent, ip_address)

        return (new_access_token, new_refresh_token, str(student_id))
