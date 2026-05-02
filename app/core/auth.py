from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4
import jwt



from app.core.config import settings


def create_access_token(student_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    delta = settings.auth.access_token_lifetime_td
    exp = now + delta
    payload = {
        'sub': str(student_id),
        'exp': int(exp.timestamp()),
        'jti': str(uuid4()),
        'iat': int(now.timestamp())
    }

    private_key = settings.auth.get_private_key()
    return jwt.encode(payload, private_key, algorithm=settings.auth.algorithm)


def create_refresh_token(
    student_id: UUID, expires_delta: timedelta | None = None
) -> str:
    now = datetime.now(timezone.utc)
    if expires_delta:
        exp = now + expires_delta
    else:
        exp = now + settings.auth.refresh_token_lifetime_td

    payload = {
        'sub': str(student_id),
        'exp': int(exp.timestamp()),
        'jti': str(uuid4()),
        'iat': int(now.timestamp())
    }

    private_key = settings.auth.get_private_key()
    return jwt.encode(payload, private_key, algorithm=settings.auth.algorithm)


def decode_token(token: str) -> dict | None:
    try:
        public_key = settings.auth.get_public_key()
        return jwt.decode(token, public_key, algorithms=[settings.auth.algorithm])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_student_id_from_token(token: str) -> Optional[UUID]:
    payload = decode_token(token)
    if payload and 'sub' in payload:
        try:
            return UUID(payload['sub'])
        except ValueError:
            return None
    return None
