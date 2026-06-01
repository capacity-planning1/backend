from uuid import UUID
from typing import Annotated

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    Request,
    Response,
    Query,
    status,
)
from fastapi.security import HTTPBearer

from app.core.auth import decode_token
from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep
from app.dependencies.services import AuthServiceDep
from app.models.students.student import StudentCreate
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.utils.errors import UnauthorizedError

router = APIRouter(prefix='/auth', tags=['auth'])
security = HTTPBearer()


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    responses=get_responses(status.HTTP_409_CONFLICT)
)
async def register(
    _request: Request,
    register_data: RegisterRequest,
    auth_service: AuthServiceDep,
):
    student = StudentCreate(
        email=register_data.email,
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        password=register_data.password,
        skills=register_data.skills
    )
    await auth_service.register(student)


@router.post(
    '/login',
    response_model=TokenResponse,
    responses=get_responses(status.HTTP_400_BAD_REQUEST)
)
async def login(
    _request: Request,
    headers: Header,
    response: Response,
    login_data: LoginRequest,
    student_session_service: AuthServiceDep,
):
    (access_token, refresh_token) = await student_session_service.login(
        email=login_data.email,
        password=login_data.password,
        user_agent=headers.get('user-agent'),
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='lax',
        max_age=settings.auth.refresh_token_lifetime_seconds,
    )
    return TokenResponse(access_token=access_token, token_type='bearer')


@router.get(
    '/me', response_model=UserResponse,
    responses=get_responses(status.HTTP_401_UNAUTHORIZED))
async def get_current_user(_request: Request, current_student: CurrentStudentDep):
    return current_student


@router.post(
    '/refresh',
    response_model=TokenResponse,
    responses=get_responses(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED)
    )
async def refresh(
    _request: Request,
    cookies: Cookie,
    headers: Header,
    response: Response,
    student_session_service: AuthServiceDep,
):
    refresh_token = cookies.get('refresh_token')

    if not refresh_token:
        raise UnauthorizedError('Refresh token not found')

    result = await student_session_service.refresh_tokens(
        refresh_token, user_agent=headers.get('user-agent')
    )

    if not result:
        raise UnauthorizedError('Invalid refresh token')

    new_access_token, new_refresh_token, _ = result

    response.set_cookie(
        key='refresh_token',
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite='lax',
    )

    return TokenResponse(access_token=new_access_token, token_type='bearer')


@router.post(
    '/logout',
    response_model=MessageResponse,
    dependencies=[Depends(CurrentStudentDep)]
)
async def logout(
    _request: Request,
    cookies: Cookie,
    response: Response,
    student_session_service: AuthServiceDep,
):
    refresh_token = cookies.get('refresh_token')
    if not refresh_token:
        raise UnauthorizedError('Token missing')

    payload = decode_token(refresh_token)
    if not payload:
        raise UnauthorizedError('Invalid token structure')

    jti = payload.get('jti')
    if not jti:
        raise UnauthorizedError('Missing required jti claim')

    await student_session_service.revoke_session(jti)
    response.delete_cookie('refresh_token', httponly=True, secure=True)

    return MessageResponse(message='Successfully logged out', success=True)


@router.post('/logout-all', response_model=MessageResponse)
async def logout_all_devices(
    _request: Request,
    response: Response,
    student_session_service: AuthServiceDep,
    current_student: CurrentStudentDep,
):
    revoked_count = await student_session_service.revoke_all_student_sessions(
        current_student.id
    )

    response.delete_cookie('refresh_token')

    return MessageResponse(
        message=f'Successfully logged out from {revoked_count} devices',
        success=True
    )


@router.post('/{student_id}/verify-email', responses=get_responses(
    status.HTTP_404_NOT_FOUND,
    status.HTTP_410_GONE)
)
async def verify_email(
    _request: Request,
    student_id: UUID,
    code: Annotated[UUID, Query()],
    auth_service: AuthServiceDep
):
    await auth_service.verify_email(student_id=student_id, code=code)


@router.post(
    '/{student_id}/change-password',
    responses=get_responses(status.HTTP_404_NOT_FOUND)
)
async def change_password(
    _request: Request,
    student_id: UUID,
    auth_serivce: AuthServiceDep
):
    await auth_serivce.send_change_password_code(student_id)


@router.post(
    '/{student_id}/confirm-change-password',
    responses=get_responses(status.HTTP_404_NOT_FOUND, status.HTTP_410_GONE)
)
async def confirm_change_password(
    _request: Request,
    student_id: UUID,
    code: Annotated[UUID, Query()],
    change_password_data: ChangePasswordRequest,
    auth_service: AuthServiceDep
):
    await auth_service.confirm_change_password(
        student_id=student_id,
        code=code,
        new_password=change_password_data.new_password,
        repeat_password=change_password_data.repeat_password
    )
