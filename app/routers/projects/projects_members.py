from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter

from app.dependencies.services import ProjectMemberServiceDep
from app.models.project import (
    ProjectMemberCreate,
    ProjectMemberPublic,
    ProjectMemberUpdate,
)
from app.schemas.projects import ProjectMembersFilters

router = APIRouter(
    prefix='/',
    tags=['projectMembers'],
)


@router.get('/{project_id}/members')
async def get_project_members(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    filters: ProjectMembersFilters
) -> Sequence[ProjectMemberPublic]:
    filters.project_id = project_id
    return await project_member_service.get_projects_members(filters)


@router.post('/{project_id}/members')
async def create_project_members(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    pm_create: ProjectMemberCreate
) -> ProjectMemberPublic:
    pm_create.project_id = project_id
    return await project_member_service.add_member_to_project(pm_create)


@router.get('/{project_id}/members/{student_id}')
async def get_project_member(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.get_project_member(student_id, project_id)


@router.put('/{project_id}/members/{student_id}')
async def update_project_member(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID,
    project_member_update: ProjectMemberUpdate
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.update_project_member(
        project_id, student_id, project_member_update
    )


@router.delete('/{project_id}/members/{student_id}')
async def delete_project_member(
    project_member_service: ProjectMemberServiceDep,
    project_id: UUID,
    student_id: UUID
) -> Optional[ProjectMemberPublic]:
    return await project_member_service.delete_project_member(
        project_id, student_id
    )
