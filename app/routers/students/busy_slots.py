from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, status

from app.core.responses import get_responses
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import BusySlotServiceDep
from app.models.students.busy_slot import (
    BusySlotCreate,
    BusySlotPublic,
    BusySlotUpdate,
)
from app.schemas.students import BusySlotFilters
from app.utils.errors import ForbiddenError
from app.utils.pagination import ListResponse

router = APIRouter(
    prefix='/{student_id}/busy-slots',
    tags=['busy_slots'],
    responses=get_responses(status.HTTP_404_NOT_FOUND)
)


@router.get('/')
async def get_busy_slots(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    student_id: UUID,
    filters: BusySlotFilters,
) -> ListResponse[BusySlotPublic]:
    if student.id != student_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    filters.student_id = student_id
    return await busy_slot_service.get_busy_slots(filters)


@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def create_busy_slot(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    student_id: UUID,
    bs_create: BusySlotCreate,
) -> BusySlotPublic:
    if student.id != student_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    bs_create.student_id = student_id
    return await busy_slot_service.create_busy_slot(bs_create)


@router.get('/{busy_slot_id}')
async def get_busy_slot(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    busy_slot_id: UUID,
) -> Optional[BusySlotPublic]:
    busy_slot = await busy_slot_service.get_busy_slot(busy_slot_id)

    if student.id != busy_slot.student_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    return busy_slot


@router.put('/{busy_slot_id}', responses=get_responses(status.HTTP_400_BAD_REQUEST))
async def update_busy_slot(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    busy_slot_id: UUID,
    bs_update: BusySlotUpdate,
) -> Optional[BusySlotPublic]:
    busy_slot = await busy_slot_service.get_busy_slot(busy_slot_id)

    if student.id != busy_slot.student_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    return await busy_slot_service.update_busy_slot(busy_slot_id, bs_update)


@router.delete('/{busy_slot_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_busy_slot(
    _request: Request,
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    busy_slot_service: BusySlotServiceDep,
    busy_slot_id: UUID,
):
    busy_slot = await busy_slot_service.get_busy_slot(busy_slot_id)

    if student.id != busy_slot.student_id or project_role != MemberRole.TEAMLEAD:
        raise ForbiddenError()

    await busy_slot_service.delete_busy_slot(busy_slot_id)
