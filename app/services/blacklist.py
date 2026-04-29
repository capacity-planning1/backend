from datetime import datetime
from uuid import UUID

from app.dependencies.repositories import (
    TokenBlacklistRepository,
    TokenBlacklistRepositoryDep,
)
from app.models.token_blacklist import TokenBlacklistModel


class BlacklistService:
    __blacklist_repo: TokenBlacklistRepository

    def __init__(self, blacklist_repo: TokenBlacklistRepositoryDep):
        self.__blacklist_repo = blacklist_repo

    async def add_token(
        self, jti: str, expires_at: datetime, student_id: UUID
    ) -> TokenBlacklistModel:
        token = TokenBlacklistModel(
            jti=jti,
            expires_at=expires_at,
            student_id=student_id,
        )

        return await self.__blacklist_repo.save(token)

    async def is_blacklisted(self, jti: str) -> bool:
        token = await self.__blacklist_repo.is_blacklisted(jti)
        return token is not None

    async def revoke_all_student_tokens(self, student_id: UUID) -> int:
        return self.__blacklist_repo.revoke_all_student_tokens(student_id)
