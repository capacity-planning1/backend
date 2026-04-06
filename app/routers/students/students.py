from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import StudentServiceDep
from app.models.students import (
    StudentPublic,
    StudentUpdate,
)
from app.routers.students import busy_slots
from app.schemas.students import StudentFilters

router = APIRouter(
    prefix='/students',
    tags=['students'],
)

router.include_router(busy_slots.router)


@router.get('/')
async def get_students(
    student_service: StudentServiceDep,
    filters: Annotated[StudentFilters, Query()]
) -> Sequence[StudentPublic]:
    return await student_service.get_students(filters)


@router.get('/profile')
async def get_student_own_profile(
    student_service: StudentServiceDep, student_id: UUID
) -> Optional[StudentPublic]:
    return await student_service.get_student(student_id)


@router.get('/{student_id}')
async def get_student_profile(
    student_service: StudentServiceDep, student_id: UUID
) -> Optional[StudentPublic]:
    return await student_service.get_student(student_id)


@router.put('/{student_id}')
async def update_student(
    student_service: StudentServiceDep,
    student_update: StudentUpdate,
    student_id: UUID
) -> Optional[StudentPublic]:
    return await student_service.update_student(student_update, student_id)


@router.delete('/{student_id}')
async def detele_student(
    student_service: StudentServiceDep, student_id: UUID
) -> Optional[StudentPublic]:
    return await student_service.delete_student(student_id)
