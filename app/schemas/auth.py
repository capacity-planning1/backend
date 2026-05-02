from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.models.students.student import StudentPublic
from app.schemas.base import CommonListFilters


class AuthBase(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    skills: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    skills: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


UserResponse = StudentPublic


class MessageResponse(BaseModel):
    message: str
    success: bool = True


class AssignRoleRequest(BaseModel):
    role_code: str = Field(..., description="Role code to assign")


class RefreshSessionFilters(CommonListFilters):
    jti: Optional[str] = None
    student_id: Optional[UUID] = None
    expires_at: Optional[datetime] = None
    is_revoked: Optional[bool] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

    _allowed_sort_fields = ['expires_at']
