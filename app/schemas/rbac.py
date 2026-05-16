from typing import Optional

from app.schemas.base import CommonListFilters


class PermissionFilters(CommonListFilters):
    code: Optional[str] = None


class RoleFilters(CommonListFilters):
    code: Optional[str] = None
