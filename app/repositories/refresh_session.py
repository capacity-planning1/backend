from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.refresh_session import RefreshSessionModel
from app.utils.repository import Repository

class RefreshSessionRepository(Repository[RefreshSessionModel]):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, 
        jti: str, student_id: UUID, expires_at: datetime,
        user_agent: str | None = None, ip_address: str | None = None) -> RefreshSessionModel:
        session = RefreshSessionModel(
            jti=jti,
            student_id=student_id,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address
        )
        self._session.add(session)
        await self._session.commit()
        await self._session.refresh(session)
        return session

    async def get_active_by_jti(self, jti: str) -> Optional[RefreshSessionModel]:
        query = select(RefreshSessionModel).where(
            RefreshSessionModel.jti == jti,
            RefreshSessionModel.is_revoked == False,
            RefreshSessionModel.expires_at > datetime.now(timezone.utc)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def revoke_session(self, jti: str) -> bool:
        query = update(RefreshSessionModel).where(
            RefreshSessionModel.jti == jti
        ).values(is_revoked=True)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount > 0

    async def revoke_all_student_sessions(self, student_id: UUID) -> int:
        query = update(RefreshSessionModel).where(
            RefreshSessionModel.student_id == student_id,
            RefreshSessionModel.is_revoked == False
        ).values(is_revoked=True)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount

