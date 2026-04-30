from datetime import datetime, timezone
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Response,
)
from fastapi.security import HTTPBearer

from app.core.auth import create_refresh_token, create_access_token, decode_token
from app.core.config import settings
from app.dependencies.auth import authenticate_student, CurrentStudentDep
from app.dependencies.services import StudentServiceDep, RefreshSessionServiceDep
from app.models.students.student import StudentCreate
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
    MessageResponse,
)

router = APIRouter(prefix='/auth', tags=['auth'])
security = HTTPBearer()


@router.post(
    '/register',
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(register_data: RegisterRequest, student_service: StudentServiceDep):
    existing_student = await student_service.get_student_by_email(register_data.email)

    if existing_student:
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
        id=student.id,
        email=student.email,
        first_name=student.first_name,
        last_name=student.last_name,
        skills=student.skills
    )


@router.post('/login', response_model=LoginResponse)
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    student_service: StudentServiceDep,
    refresh_session_service: RefreshSessionServiceDep):
    student = await authenticate_student(
        login_data.email, login_data.password, student_service
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
        )

    access_token = create_access_token(student.id)
    refresh_token = create_refresh_token(student.id)

    refresh_payload = decode_token(refresh_token)

    if not refresh_payload:
        raise HTTPException(status_code=500, detail="Invalid token payload")

    await refresh_session_service.create_session(
        jti=refresh_payload.get("jti"),
        student_id=student.id,
        expires_at = datetime.fromtimestamp(float(refresh_payload["exp"]), tz=timezone.utc),
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.auth.refresh_token_lifetime_seconds
    )
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.get('/me', response_model=UserResponse)
async def get_current_user(
    current_student: CurrentStudentDep
):
    return current_student


@router.post('/refresh', response_model=LoginResponse)
async def refresh(
    request: Request,
    response: Response,
    refresh_session_service: RefreshSessionServiceDep
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    result = await refresh_session_service.refresh_tokens(
        refresh_token,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None
    )

    if not result:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token, new_refresh_token, _ = result

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return LoginResponse(access_token=new_access_token, refresh_token=new_refresh_token)


@router.post('/logout', response_model=MessageResponse)
async def logout(
    response: Response,
    request: Request,
    refresh_session_service: RefreshSessionServiceDep
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        payload = decode_token(refresh_token)
        if payload:
            jti = payload.get("jti")
            if jti:
                await refresh_session_service.revoke_session(jti)

    response.delete_cookie("refresh_token")

    return MessageResponse(
        message="Successfully logged out",
        success=True
    )

@router.post("/logout-all", response_model=MessageResponse)
async def logout_all_devices(
    response: Response,
    refresh_session_service: RefreshSessionServiceDep,
    current_student: CurrentStudentDep
):
    revoked_count = await refresh_session_service.revoke_all_student_sessions(current_student.id)

    response.delete_cookie("refresh_token")

    return MessageResponse(
        message=f"Successfully logged out from {revoked_count} devices",
        success=True
    )