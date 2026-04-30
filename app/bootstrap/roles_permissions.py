from typing import Dict
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.rbac import RoleModel, PermissionModel
from app.repositories.rbac import RoleRepository, PermissionRepository
from app.core.config import settings


PERMISSIONS_CONFIG = {
    "students:read": {"name": "View students", "description": "Get list or single student"},
    "students:write": {"name": "Manage students", "description": "Create, update, delete students"},

    "projects:read": {"name": "View projects", "description": "Get list or single project"},
    "projects:write": {"name": "Manage projects", "description": "Create, update, delete projects, join project"},

    "teams:read": {"name": "View teams", "description": "Get teams list or details"},
    "teams:write": {"name": "Manage teams", "description": "Create, update, delete teams"},

    "project_members:read": {"name": "View project members", "description": "Get members list or details"},
    "project_members:write": {"name": "Manage project members", "description": "Add, update, remove members"},

    "team_memberships:read": {"name": "View team memberships", "description": "Get membership list"},
    "team_memberships:write": {"name": "Manage team memberships", "description": "Add, update, remove members in team"},

    "tasks:read": {"name": "View tasks", "description": "Get tasks list or details"},
    "tasks:write": {"name": "Manage tasks", "description": "Create, update, delete tasks, assign tasks"},

    "busy_slots:read": {"name": "View busy slots", "description": "Get busy slots of a student"},
    "busy_slots:write": {"name": "Manage busy slots", "description": "Create, update, delete busy slots"},

    "change_requests:read": {"name": "View change requests", "description": "Get change requests list"},
    "change_requests:write": {"name": "Manage change requests", "description": "Create, update, delete change requests"},

    "sprints:read": {"name": "View sprints", "description": "Get sprints list or details"},
    "sprints:write": {"name": "Manage sprints", "description": "Create, update, delete sprints"},

    "admin:users": {"name": "Manage all users", "description": "Full user management"},
    "admin:roles": {"name": "Manage roles and permissions", "description": "Assign/remove roles"},
    "admin:*": {"name": "Full admin access", "description": "All permissions"},
}

ROLES_CONFIG = {
    "admin": {
        "name": "System Administrator",
        "description": "Full system access with all permissions",
        "is_system": True,
        "permissions": ["admin:*"],
    },
    "user": {
        "name": "User",
        "description": "Default role for all registered users",
        "is_system": True,
        "permissions": [
            "profile:read",
            "profile:update",
            "project:list",
            "project:join",
        ],
    },
}


async def bootstrap_roles_permissions(session: AsyncSession):
    role_repo = RoleRepository(session)
    permission_repo = PermissionRepository(session)
    created_permissions: Dict[str, PermissionModel] = {}
    for code, perm_data in PERMISSIONS_CONFIG.items():
        permission = await permission_repo.get_or_create(
            code=code,
            name=perm_data["name"],
            description=perm_data.get("description")
        )
        created_permissions[code] = permission
        print(f"  ✓ Permission: {code}")

    created_roles: Dict[str, RoleModel] = {}
    for role_code, role_data in ROLES_CONFIG.items():
        existing_role = await role_repo.get_by_code(role_code)

        if not existing_role:
            role = RoleModel(
                name=role_data["name"],
                code=role_code,
                description=role_data["description"],
                is_system=role_data["is_system"],
            )
            role = await role_repo.save(role)
            created_roles[role_code] = role
            print(f"  ✓ Role created: {role_code}")
        else:
            created_roles[role_code] = existing_role
            print(f"  ✓ Role exists: {role_code}")

        role = created_roles[role_code]
        current_perms = {p.code for p in role.permissions}
        target_perms = set(role_data["permissions"])

        for perm_code in target_perms - current_perms:
            if perm_code in created_permissions:
                role.permissions.append(created_permissions[perm_code])
                print(f"    → Added permission {perm_code} to {role_code}")
            elif perm_code == "admin:*":
                for p_code, p_perm in created_permissions.items():
                    if p_code not in current_perms:
                        role.permissions.append(p_perm)
                        print(f"    → Added permission {p_code} to {role_code}")
        if target_perms - current_perms:
            await role_repo.save(role)
    return created_roles, created_permissions
