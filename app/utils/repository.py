from typing import Generic, Optional, Sequence, TypeAlias, TypeVar
from uuid import UUID

from app.dependencies.session import SessionDep
from generics import get_filled_type
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.sql._typing import _ColumnExpressionArgument
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.base import BaseModel


FilterType: TypeAlias = _ColumnExpressionArgument[bool] | bool

ModelT = TypeVar('ModelT', bound=BaseModel)


class Repository(Generic[ModelT]):
    __model: type[ModelT] | None = None
    __session: AsyncSession

    @property
    def model(self) -> type[ModelT]:
        if self.__model is None:
            self.__model = get_filled_type(self, Repository, 0)
        return self.__model

    def __init__(self, session: SessionDep):
        self.__session = session

    async def get(self, pk: UUID) -> Optional[ModelT]:
        return await self.__session.get(self.model, pk)

    async def fetch(
        self,
        filters: Optional[PydanticBaseModel] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Sequence[ModelT]:
        select_statement = select(self.model)
        if filters is not None:
            filters_statement = and_(True)
            filters_dict = filters.model_dump()
            for key, value in filters_dict.items():
                if not hasattr(self.__model, key):
                    continue
                if value is not None:
                    filters_statement = and_(
                        filters_statement, getattr(self.__model, key) == value
                    )
            select_statement = select_statement.where(filters_statement)
        if offset is not None:
            select_statement = select_statement.offset(offset)
        if limit is not None:
            select_statement = select_statement.limit(limit)
        entities = await self.__session.exec(select_statement)
        return entities.all()

    async def save(self, instance: ModelT) -> ModelT:
        self.__session.add(instance)
        await self.__session.commit()
        await self.__session.refresh(instance)
        return instance

    async def save_all(self, instanses: list[ModelT]) -> list[ModelT]:
        self.__session.add_all(instanses)
        await self.__session.commit()
        for instance in instanses:
            await self.__session.refresh(instance)
        return instanses

    async def delete(self, pk: UUID) -> Optional[ModelT]:
        instance = await self.get(pk)
        if instance is None:
            return instance
        await self.__session.delete(instance)
        await self.__session.commit()
        return instance

    async def update(self, pk: UUID, updates: PydanticBaseModel) -> Optional[ModelT]:
        instance = await self.get(pk)
        if instance is None:
            return None
        instance_update_dump = updates.model_dump()
        for key, value in instance_update_dump.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await self.save(instance)
        return instance
