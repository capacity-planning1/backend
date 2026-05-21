from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.dependencies.services import StudentServiceDep
from app.schemas.auth import AssignRoleRequest, MessageResponse
from app.core.config import settings

router = APIRouter(prefix='/roles', tags=['roles'])


@router.post('/assign/{student_id}', response_model=MessageResponse)
async def assign_role_to_user(
    student_id: UUID,
    request: AssignRoleRequest,
    student_service: StudentServiceDep,
):
    student = await student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail='User not found')

    student.role = request.role_code

    success = await student_service.update_student(student)

    if not success:
        raise HTTPException(status_code=400, detail='Failed to assign role')

    return MessageResponse(
        message=f'Role {request.role_code} assigned to user {student_id}'
    )


@router.delete('/{student_id}', response_model=MessageResponse)
async def remove_role_from_user(
    student_id: UUID,
    request: AssignRoleRequest,
    student_service: StudentServiceDep
):
    student = await student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail='User not found')

    student.role = settings.role.default_user_role_code
    success = await student_service.update_student(student)

    if not success:
        raise HTTPException(status_code=400, detail='Failed to remove role')

    return MessageResponse(
        message=f'Role {request.role_code} removed from user {student_id}'
    )