from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

T_co = TypeVar('T_co', covariant=True)


class PaginationInfo(SQLModel):
    page: int
    page_num: int
    total: int


class ListResponse(BaseModel, Generic[T_co]):
    info: PaginationInfo
    items: Sequence[T_co]
