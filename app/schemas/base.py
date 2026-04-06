from typing import Literal, Optional

from pydantic import BaseModel, field_validator


class CommonListFilters(BaseModel):
    offset: int = 0
    limit: int = 10
    sort_by: Optional[str] = None
    sort_order: Literal['asc', 'desc'] = 'asc'
    _allowed_sort_fields: list[str] = []

    @field_validator('sort_by')
    def validate_sort_field(self, v):
        if v is None:
            return v

        if v not in self._allowed_sort_fields:
            raise ValueError(
                f"Project sorting by '{v}' not allowed. Allowed: {self._allowed_sort_fields}"
            )
        return v
