from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.auth import create_access_token, decode_token, get_student_id_from_token
from app.dependencies.services import StudentServiceDep, TokenBlacklistServiceDep
from app.models.students.student import StudentModel, StudentPublic
from app.utils.hasher import Hasher

oauth2_scheme = HTTPBearer(auto_error=False)

type AuthenticatedStudent = Optional[StudentPublic]


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
) -> StudentPublic:
    if not credentials:
        raise HTTPException(status_code=401, detail='Not authenticated')

    student_id = get_student_id_from_token(credentials.credentials)

    if not student_id:
        raise HTTPException(status_code=401, detail='Invalid token')

    student = await student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=401, detail='User not found')

    return StudentPublic(
        id=student.id,
        email=student.email,
        first_name=student.first_name,
        last_name=student.last_name,
        skills=student.skills,
        created_at=student.created_at,
        updated_at=student.updated_at
    )


CurrentStudentDep = Annotated[StudentPublic, Depends(get_current_student)]
