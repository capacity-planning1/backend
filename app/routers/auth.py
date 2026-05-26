from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import HTTPBearer

from app.core.auth import decode_token
from app.core.config import settings
from app.dependencies.auth import CurrentStudentDep
from app.dependencies.services import StudentServiceDep, StudentSessionServiceDep
from app.models.students.student import StudentCreate
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix='/auth', tags=['auth'])
security = HTTPBearer()


@router.post(
    '/register', response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    _request: Request,
    register_data: RegisterRequest,
    student_service: StudentServiceDep,
):
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
        skills=student.skills,
    )


@router.post('/login', response_model=TokenResponse)
async def login(
    _request: Request,
    headers: Header,
    response: Response,
    login_data: LoginRequest,
    student_session_service: StudentSessionServiceDep,
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


@router.get('/me', response_model=UserResponse)
async def get_current_user(_request: Request, current_student: CurrentStudentDep):
    return current_student


@router.post('/refresh', response_model=TokenResponse)
async def refresh(
    _request: Request,
    cookies: Cookie,
    headers: Header,
    response: Response,
    student_session_service: StudentSessionServiceDep,
):
    refresh_token = cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh token not found')

    result = await student_session_service.refresh_tokens(
        refresh_token, user_agent=headers.get('user-agent')
    )

    if not result:
        raise HTTPException(status_code=401, detail='Invalid refresh token')

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
    '/logout', response_model=MessageResponse, dependencies=[Depends(CurrentStudentDep)]
)
async def logout(
    _request: Request,
    cookies: Cookie,
    response: Response,
    student_session_service: StudentSessionServiceDep,
):
    refresh_token = cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Token missing')

    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid token structure')

    jti = payload.get('jti')
    if not jti:
        raise HTTPException(status_code=401, detail='Missing required jti claim')

    await student_session_service.revoke_session(jti)
    response.delete_cookie('refresh_token', httponly=True, secure=True)

    return MessageResponse(message='Successfully logged out', success=True)


@router.post('/logout-all', response_model=MessageResponse)
async def logout_all_devices(
    _request: Request,
    response: Response,
    student_session_service: StudentSessionServiceDep,
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
