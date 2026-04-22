from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import ProjectMemberServiceDep
from app.models.projects.project import (
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
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    filters: ProjectMembersFilters
) -> Sequence[ProjectMemberPublic]:
    filters.project_id = project_id
    return await project_member_service.get_projects_members(filters)


@router.post('/')
async def create_project_members(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    pm_create: ProjectMemberCreate
) -> ProjectMemberPublic:
    pm_create.project_id = project_id
    return await project_member_service.add_member_to_project(pm_create)


@router.get('/{student_id}')
async def get_project_member(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID
) -> Optional[ProjectMemberPublic]:
    filters = ProjectMembersFilters()
    filters.project_id = project_id
    filters.student_id = student_id
    return await project_member_service.get_project_member(filters)


@router.put('/{student_id}')
async def update_project_member(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
    project_member_update: ProjectMemberUpdate
) -> Optional[ProjectMemberPublic]:
    filters = ProjectMembersFilters()
    filters.student_id = student_id
    filters.project_id = project_id
    return await project_member_service.update_project_member(
        filters, project_member_update
    )


@router.delete('/{student_id}')
async def delete_project_member(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID
) -> Optional[ProjectMemberPublic]:
    filters = ProjectMembersFilters()
    filters.project_id = project_id
    filters.student_id = student_id
    return await project_member_service.delete_project_member(filters)
