from typing import Optional
from uuid import UUID

from app.dependencies.repositories import (
    BusySlotRepository,
    BusySlotRepositoryDep,
)
from app.models.students.busy_slot import (
    BusySlotCreate,
    BusySlotModel,
    BusySlotPublic,
    BusySlotUpdate,
)
from app.schemas.students import BusySlotFilters
from app.utils.pagination import ListResponse
from app.utils.errors import NotFoundError


class BusySlotService:
    __busy_slot_repository: BusySlotRepository

    def __init__(self, bs_repository: BusySlotRepositoryDep):
        self.__busy_slot_repository = bs_repository

    async def get_busy_slots(
        self, filters: BusySlotFilters
    ) -> ListResponse[BusySlotPublic]:
        return await self.__busy_slot_repository.fetch(filters)

    async def create_busy_slot(self, bs_create: BusySlotCreate) -> BusySlotPublic:
        bs_dump = bs_create.model_dump()
        bs = BusySlotModel(**bs_dump)
        return await self.__busy_slot_repository.save(bs)

    async def get_busy_slot(self, bs_id: UUID) -> Optional[BusySlotPublic]:
        result = await self.__busy_slot_repository.get(bs_id)
        if result is None:
            raise NotFoundError()
        return result

    async def update_busy_slot(
        self, bs_id: UUID, bs_update: BusySlotUpdate
    ) -> Optional[BusySlotPublic]:
        result = await self.__busy_slot_repository.update(bs_id, bs_update)
        if result is None:
            raise NotFoundError()
        return await self.__busy_slot_repository.update(bs_id, bs_update)

    async def delete_busy_slot(self, bs_id: UUID) -> Optional[BusySlotPublic]:
        result = await self.__busy_slot_repository.delete(bs_id)
        if result is None:
            raise NotFoundError()
        return result
