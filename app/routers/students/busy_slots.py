from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import BusySlotServiceDep
from app.models.students.busy_slot import (
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
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    student_id: UUID,
    filters: BusySlotFilters
) -> Sequence[BusySlotPublic]:
    if (
        student.id != student_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters.student_id = student_id
    return await busy_slot_service.get_busy_slots(filters)


@router.post('/')
async def create_busy_slot(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    student_id: UUID,
    bs_create: BusySlotCreate
) -> BusySlotPublic:
    if (
        student.id != student_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    bs_create.student_id = student_id
    return await busy_slot_service.create_busy_slot(bs_create)


@router.get('/{busy_slot_id}')
async def get_busy_slot(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    busy_slot_id: UUID
) -> Optional[BusySlotPublic]:
    busy_slot = await busy_slot_service.get_busy_slot(busy_slot_id)

    if (
        student.id != busy_slot.student_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return busy_slot


@router.put('/{busy_slot_id}')
async def update_busy_slot(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    busy_slot_id: UUID,
    bs_update: BusySlotUpdate,
) -> Optional[BusySlotPublic]:
    busy_slot = await busy_slot_service.get_busy_slot(busy_slot_id)

    if (
        student.id != busy_slot.student_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await busy_slot_service.update_busy_slot(busy_slot_id, bs_update)


@router.delete('/{busy_slot_id}')
async def delete_busy_slot(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    busy_slot_id: UUID
) -> Optional[BusySlotPublic]:
    busy_slot = await busy_slot_service.get_busy_slot(busy_slot_id)

    if (
        student.id != busy_slot.student_id
        or project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await busy_slot_service.delete_busy_slot(busy_slot_id)
