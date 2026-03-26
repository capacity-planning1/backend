from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import BusySlotServiceDep, StudentServiceDep
from app.models.students import (
    BusySlotCreate,
    BusySlotPublic,
    BusySlotUpdate,
    StudentPublic,
    StudentUpdate,
)
from app.schemas.students import BusySlotFilters, StudentFilters

router = APIRouter(
    prefix='/students',
    tags=['students'],
)


@router.get('/')
async def get_students(
    student_service: StudentServiceDep, filters: Annotated[StudentFilters, Query()]
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
    student_service: StudentServiceDep, student_update: StudentUpdate, student_id: UUID
) -> Optional[StudentPublic]:
    return await student_service.update_student(student_update, student_id)


@router.delete('/{student_id}')
async def detele_student(
    student_service: StudentServiceDep, student_id: UUID
) -> Optional[StudentPublic]:
    return await student_service.delete_student(student_id)


@router.get('/{student_id}/busy-slots')
async def get_busy_slots(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, filters: BusySlotFilters
) -> Sequence[BusySlotPublic]:
    filters.student_id = student_id
    return await busy_slot_service.get_busy_slots(filters)


@router.post('/{student_id}/busy-slots')
async def create_busy_slot(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, bs_create: BusySlotCreate
) -> BusySlotPublic:
    bs_create.student_id = student_id
    return await busy_slot_service.create_busy_slot(bs_create)


@router.get('/{student_id}/busy-slots/{busy_slot_id}')
async def get_busy_slot(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, busy_slot_id: UUID
) -> Optional[BusySlotPublic]:
    return await busy_slot_service.get_busy_slot(busy_slot_id)


@router.put('/{student_id}/busy-slots/{busy_slot_id}')
async def update_busy_slot(
    busy_slot_service: BusySlotServiceDep,
    student_id: UUID,
    busy_slot_id: UUID,
    bs_update: BusySlotUpdate,
) -> Optional[BusySlotPublic]:
    return await busy_slot_service.update_busy_slot(busy_slot_id, bs_update)


@router.delete('/{student_id}/busy-slots/{busy_slot_id}')
async def delete_busy_slot(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, busy_slot_id: UUID
) -> Optional[BusySlotPublic]:
    return await busy_slot_service.delete_busy_slot(busy_slot_id)
