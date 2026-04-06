from typing import Any, Generic, Optional, Sequence, TypeAlias, TypeVar
from uuid import UUID

from generics import get_filled_type
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.sql._typing import _ColumnExpressionArgument
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.session import SessionDep
from app.models.base import BaseModel

FilterType: TypeAlias = _ColumnExpressionArgument[bool] | bool

ModelT = TypeVar('ModelT', bound=BaseModel)


class Repository(Generic[ModelT]):
    __model: type[ModelT] | None = None
    __session: AsyncSession
    OFFSET = 0
    LIMIT = 100

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
    ) -> Sequence[ModelT]:
        select_statement = select(self.model)

        offset = self.OFFSET
        limit = self.LIMIT

        if filters is not None:
            filter_data = filters.model_dump(
                exclude={'offset', 'limit', 'sort_by', 'sort_order'}, exclude_none=True
            )

            for key, value in filter_data.items():
                if hasattr(self.model, key):
                    select_statement = select_statement.where(
                        getattr(self.model, key) == value
                    )

            sort_by = getattr(filters, 'sort_by', None)
            if sort_by and hasattr(self.model, sort_by):
                column = getattr(self.model, sort_by)
                sort_order = getattr(filters, 'sort_order', 'asc')
                select_statement = select_statement.order_by(
                    column.desc() if sort_order == 'desc' else column.asc()
                )

            offset = getattr(filters, 'offset', 0)
            limit = getattr(filters, 'limit', 100)

        select_statement = select_statement.offset(offset).limit(limit)
        result = await self.__session.execute(select_statement)
        return result.scalars().all()

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

    async def fetch_by_related_project(
        self,
        related_model: type,
        current_foreign_key: str,
        related_filter_field: str,
        related_filter_value: Any,
        filters: Optional[PydanticBaseModel] = None,
    ) -> Sequence[ModelT]:
        """
        Получить все сущности ModelT, у которых через связанную модель
        поле related_filter_field равно related_filter_value
        Args:
            related_model: Класс связанной модели
            current_foreign_key: Имя поля в текущей модели
            related_filter_field: Имя поля в связанной модели для фильтрации
            related_filter_value: Значение для фильтрации по связанной модели
            filters: Pydantic модель с фильтрами для основной модели
        """
        current_field = getattr(self.model, current_foreign_key)
        related_id_field = related_model.id
        related_filter_attr = getattr(related_model, related_filter_field)

        select_statement = (
            select(self.model)
            .join(related_model, current_field == related_id_field)
            .where(related_filter_attr == related_filter_value)
        )

        offset = self.OFFSET
        limit = self.LIMIT

        if filters is not None:
            filter_data = filters.model_dump(
                exclude={'offset', 'limit', 'sort_by', 'sort_order'}, exclude_none=True
            )

            for key, value in filter_data.items():
                if hasattr(self.model, key):
                    select_statement = select_statement.where(
                        getattr(self.model, key) == value
                    )

            sort_by = getattr(filters, 'sort_by', None)
            if sort_by and hasattr(self.model, sort_by):
                column = getattr(self.model, sort_by)
                sort_order = getattr(filters, 'sort_order', 'asc')
                select_statement = select_statement.order_by(
                    column.desc() if sort_order == 'desc' else column.asc()
                )

            offset = getattr(filters, 'offset', 0)
            limit = getattr(filters, 'limit', 100)

        select_statement = select_statement.offset(offset).limit(limit)
        result = await self.__session.execute(select_statement)
        return result.scalars().all()
