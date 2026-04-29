from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPAuthorizationCredentials,
    HTTPException,
    status,
)

from app.core.auth import create_refresh_token, create_student_access_token
from app.dependencies.auth import authenticate_student, refresh_access_token
from app.dependencies.services import StudentServiceDep, TokenBlacklistServiceDep
from app.models.students.student import StudentCreate
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
)

router = APIRouter(prefix='/auth', tags=['auth'])
security = HTTPBearer()


@router.post('/register', response_model=RegisterResponse)
async def register(register_data: RegisterRequest, student_service: StudentServiceDep):
    student = await student_service.get_student_by_email(register_data.email)

    if student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exists',
        )

    student_create = StudentCreate(
        email=register_data.email,
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        skills=register_data.skills,
        password=register_data.password,
    )

    student = await student_service.create_student(student_create)

    return RegisterResponse(
        id=str(student.id),
        email=student.email,
        first_name=student.first_name,
        last_name=student.last_name,
    )


@router.post('/login', response_model=LoginResponse)
async def login(login_data: LoginRequest, student_service: StudentServiceDep):
    student = await authenticate_student(
        login_data.email, login_data.password, student_service
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
        )

    access_token = create_student_access_token(student.id)
    refresh_token = create_refresh_token(student.id)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post('/refresh', response_model=LoginResponse)
async def refresh(refresh_data: RefreshRequest, student_service: StudentServiceDep):
    new_access_token = await refresh_access_token(
        refresh_data.refresh_token, student_service
    )

    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token',
        )

    return LoginResponse(
        access_token=new_access_token, refresh_token=refresh_data.refresh_token
    )


@router.post('/logout')
async def logout(
    blacklist_service: TokenBlacklistServiceDep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    await blacklist_service.add_token(credentials.credentials)
