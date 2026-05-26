from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.core.config import settings
from app.dependencies.auth import CurrentStudentDep
from app.dependencies.services import StudentServiceDep
from app.models.students.student import (
    StudentPublic,
    StudentUpdate,
)
from app.routers.students import busy_slots
from app.schemas.students import StudentFilters
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/students',
    tags=['students'],
)

router.include_router(busy_slots.router)


@router.get('/', dependencies=[Depends(CurrentStudentDep)])
async def get_students(
    _request: Request,
    student_service: StudentServiceDep,
    filters: Annotated[StudentFilters, Query()],
) -> ListResponse[StudentPublic]:
    return await student_service.get_students(filters)


@router.get('/profile')
async def get_student_own_profile(
    _request: Request, student: CurrentStudentDep, student_service: StudentServiceDep
) -> Optional[StudentPublic]:
    return await student_service.get_student(student.id)


@router.get('/{student_id}')
async def get_student_profile(
    _request: Request, student_service: StudentServiceDep, student_id: UUID
) -> Optional[StudentPublic]:
    return await student_service.get_student(student_id)


@router.put('/{student_id}')
async def update_student(
    _request: Request,
    student: CurrentStudentDep,
    student_service: StudentServiceDep,
    student_update: StudentUpdate,
    student_id: UUID,
) -> Optional[StudentPublic]:
    if student.id != student_id or student.role != settings.role.admin_role_code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await student_service.update_student(student_update, student_id)


@router.delete('/{student_id}')
async def detele_student(
    _request: Request,
    student: CurrentStudentDep,
    student_service: StudentServiceDep,
    student_id: UUID,
) -> Optional[StudentPublic]:
    if student.id != student_id or student.role != settings.role.admin_role_code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await student_service.delete_student(student_id)
