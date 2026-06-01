from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

T = TypeVar('T', covariant=True)


class PaginationInfo(SQLModel):
    page: int
    page_num: int
    total: int


class ListResponse(BaseModel, Generic[T]):
    info: PaginationInfo
    items: Sequence[T]
