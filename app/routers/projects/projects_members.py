from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.dependencies.auth import CurrentStudentDep, MemberRole, ProjectRoleDep
from app.dependencies.services import ProjectMemberServiceDep
from app.models.projects.project_member import (
    ProjectMemberCreate,
    ProjectMemberPublic,
    ProjectMemberUpdate,
)
from app.schemas.projects import ProjectMembersFilters

router = APIRouter(
    prefix='/{project_id}/members',
    tags=['projectMembers'],
)


@router.get('/')
async def get_project_members(
    student: CurrentStudentDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    filters: ProjectMembersFilters,
    project_role: ProjectRoleDep,
) -> Sequence[ProjectMemberPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters.project_id = project_id
    return await project_member_service.get_projects_members(filters)


@router.post('/')
async def create_project_members(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    pm_create: ProjectMemberCreate,
) -> ProjectMemberPublic:
    if (
        student.role == settings.role.default_user_role_code
        and project_role != MemberRole.TEAMLEAD
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    pm_create.project_id = project_id
    return await project_member_service.add_member_to_project(pm_create)


@router.get('/{student_id}')
async def get_project_member(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
) -> Optional[ProjectMemberPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters = ProjectMembersFilters()
    filters.project_id = project_id
    filters.student_id = student_id
    return await project_member_service.get_project_member(filters)


@router.put('/{student_id}')
async def update_project_member(  # noqa: PLR0913
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
    project_member_update: ProjectMemberUpdate,
) -> Optional[ProjectMemberPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if student.id != student_id or student.role != MemberRole.TEAMLEAD:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters = ProjectMembersFilters()
    filters.student_id = student_id
    filters.project_id = project_id
    return await project_member_service.update_project_member(
        filters, project_member_update
    )


@router.delete('/{student_id}')
async def delete_project_member(
    student: CurrentStudentDep,
    project_role: ProjectRoleDep,
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
) -> Optional[ProjectMemberPublic]:
    if (
        student.role == settings.role.default_user_role_code
        and project_role == MemberRole.OTHER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if student.id != student_id or student.role != MemberRole.TEAMLEAD:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    filters = ProjectMembersFilters()
    filters.project_id = project_id
    filters.student_id = student_id
    return await project_member_service.delete_project_member(filters)
