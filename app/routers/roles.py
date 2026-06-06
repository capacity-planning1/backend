from uuid import UUID

from fastapi import APIRouter, Request, status

from app.core.config import settings
from app.core.responses import get_responses
from app.dependencies.services import StudentServiceDep
from app.schemas.auth import AssignRoleRequest, MessageResponse
from app.utils.errors import BadRequestError, NotFoundError

router = APIRouter(
    prefix='/roles',
    tags=['roles'],
    responses=get_responses(
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
    ),
)


@router.post('/assign/{student_id}', response_model=MessageResponse)
async def assign_role_to_user(
    _request: Request,
    student_id: UUID,
    request: AssignRoleRequest,
    student_service: StudentServiceDep,
):
    student = await student_service.get_student(student_id)
    if not student:
        raise NotFoundError('User not found')

    student.role = request.role_code

    success = await student_service.update_student(student)

    if not success:
        raise BadRequestError('Failed to assign role')

    return MessageResponse(
        message=f'Role {request.role_code} assigned to user {student_id}'
    )


@router.delete('/{student_id}', response_model=MessageResponse)
async def remove_role_from_user(
    _request: Request,
    student_id: UUID,
    request: AssignRoleRequest,
    student_service: StudentServiceDep,
):
    student = await student_service.get_student(student_id)
    if not student:
        raise NotFoundError('User not found')

    student.role = settings.role.default_user_role_code
    success = await student_service.update_student(student)

    if not success:
        raise BadRequestError('Failed to remove role')

    return MessageResponse(
        message=f'Role {request.role_code} removed from user {student_id}'
    )
