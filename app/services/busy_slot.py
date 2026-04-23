from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    BusySlotRepository,
    BusySlotRepositoryDep,
)
from app.models.students import (
    BusySlotCreate,
    BusySlotModel,
    BusySlotPublic,
    BusySlotUpdate,
)
from app.schemas.students import BusySlotFilters


class BusySlotService:
    __busy_slot_repository: BusySlotRepository

    def __init__(self, bs_repository: BusySlotRepositoryDep):
        self.__busy_slot_repository = bs_repository

    async def get_busy_slots(
        self, filters: BusySlotFilters
    ) -> Sequence[BusySlotPublic]:
        return await self.__busy_slot_repository.fetch(filters)

    async def create_busy_slot(self, bs_create: BusySlotCreate) -> BusySlotPublic:
        bs_dump = bs_create.model_dump()
        bs = BusySlotModel(**bs_dump)
        return await self.__busy_slot_repository.save(bs)

    async def get_busy_slot(self, bs_id: UUID) -> Optional[BusySlotPublic]:
        return await self.__busy_slot_repository.get(bs_id)

    async def update_busy_slot(
        self, bs_id: UUID, bs_update: BusySlotUpdate
    ) -> Optional[BusySlotPublic]:
        return await self.__busy_slot_repository.update(bs_id, bs_update)

    async def delete_busy_slot(self, bs_id: UUID) -> Optional[BusySlotPublic]:
        return await self.__busy_slot_repository.delete(bs_id)
