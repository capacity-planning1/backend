from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.auth import create_access_token, decode_token, get_student_id_from_token
from app.dependencies.services import StudentServiceDep, TokenBlacklistServiceDep
from app.models.students.student import StudentModel
from app.utils.hasher import Hasher

oauth2_scheme = HTTPBearer(auto_error=False)

type AuthenticatedStudent = Optional[StudentModel]


async def authenticate_student(
    email: str, password: str, student_service: StudentServiceDep
) -> AuthenticatedStudent:
    student = await student_service.get_student_by_email(email)

    if not student:
        return None

    if Hasher.verify_password(password, student.hashed_password):
        return student

    return None


async def get_current_student(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(oauth2_scheme)
    ],
    student_service: StudentServiceDep,
    blacklist_service: TokenBlacklistServiceDep,
) -> StudentModel:
    if not credentials:
        raise HTTPException(status_code=401, detail='Not authenticated')

    student_id = get_student_id_from_token(credentials.credentials)

    if not student_id:
        raise HTTPException(status_code=401, detail='Invalid token')

    student = await student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=401, detail='User not found')

    return student


CurrentStudentDep = Annotated[StudentModel, Depends(get_current_student)]


async def refresh_access_token(
    refresh_token: str, student_service: StudentServiceDep
) -> str | None:
    payload = decode_token(refresh_token)
    if not payload:
        return None

    student_id = payload.get('sub')
    if not student_id:
        return None

    student = await student_service.get_student(student_id)
    if not student:
        return None

    return create_access_token(student_id)
