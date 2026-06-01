from typing import ClassVar, Optional

from pydantic import PrivateAttr
from sqlmodel import Field, SQLModel

from app.utils.errors import (
    BadRequestError,
    ConflictError,
    GoneError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
)


class ErrorSchema(SQLModel):
    detail: Optional[dict] = Field(default_factory=dict)
    message: str
    _error_cls: ClassVar[type[Exception]] = PrivateAttr(default=Exception)

    @property
    def error_cls(self) -> type[Exception]:
        return self._error_cls


class NotFoundErrorSchema(ErrorSchema):
    _error_cls: ClassVar[type[Exception]] = NotFoundError
    message: str = NotFoundError.message


class ForbiddenErrorSchema(ErrorSchema):
    _error_cls: ClassVar[type[Exception]] = ForbiddenError
    message: str = ForbiddenError.message


class UnauthorizedErrorSchema(ErrorSchema):
    _error_cls: ClassVar[type[Exception]] = UnauthorizedError
    message: str = UnauthorizedError.message


class InternalServerErrorSchema(ErrorSchema):
    _error_cls: ClassVar[type[Exception]] = InternalServerError
    message: str = InternalServerError.message


class BadRequestErrorSchema(ErrorSchema):
    _error_cls: ClassVar[type[Exception]] = BadRequestError
    message: str = BadRequestError.message


class ConflictErrorSchema(ErrorSchema):
    _error_cls: ClassVar[type[Exception]] = ConflictError
    message: str = ConflictError.message


class GoneErrorSchema(ErrorSchema):
    _error_cls: ClassVar[type[Exception]] = GoneError
    message: str = GoneError.message
