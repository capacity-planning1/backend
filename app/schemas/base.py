from typing import Literal, Optional

from pydantic import BaseModel


class CommonListFilters(BaseModel):
    offset: int = 0
    limit: int = 10
    sort_by: Optional[str] = None
    sort_order: Literal["asc", "desc"] = "asc"
