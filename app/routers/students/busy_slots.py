from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import BusySlotServiceDep
from app.models.students import (
    BusySlotCreate,
    BusySlotPublic,
    BusySlotUpdate,
)
from app.schemas.students import BusySlotFilters

router = APIRouter(
    prefix='/{student_id}/busy-slots',
    tags=['busy_slots'],
)


@router.get('/')
async def get_busy_slots(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, filters: BusySlotFilters
) -> Sequence[BusySlotPublic]:
    filters.student_id = student_id
    return await busy_slot_service.get_busy_slots(filters)


@router.post('/')
async def create_busy_slot(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, bs_create: BusySlotCreate
) -> BusySlotPublic:
    bs_create.student_id = student_id
    return await busy_slot_service.create_busy_slot(bs_create)


@router.get('/{busy_slot_id}')
async def get_busy_slot(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, busy_slot_id: UUID
) -> Optional[BusySlotPublic]:
    return await busy_slot_service.get_busy_slot(busy_slot_id)


@router.put('/{busy_slot_id}')
async def update_busy_slot(
    busy_slot_service: BusySlotServiceDep,
    student_id: UUID,
    busy_slot_id: UUID,
    bs_update: BusySlotUpdate,
) -> Optional[BusySlotPublic]:
    return await busy_slot_service.update_busy_slot(busy_slot_id, bs_update)


@router.delete('/{busy_slot_id}')
async def delete_busy_slot(
    busy_slot_service: BusySlotServiceDep, student_id: UUID, busy_slot_id: UUID
) -> Optional[BusySlotPublic]:
    return await busy_slot_service.delete_busy_slot(busy_slot_id)
