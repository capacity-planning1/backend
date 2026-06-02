import asyncio

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.database import engine
from app.models.students.student import StudentModel
from app.schemas.students import StudentFilters
from app.utils.hasher import Hasher
from app.utils.repository import Repository


async def create_admin_user(session: AsyncSession):
    student_repo = Repository[StudentModel](session)
    student_repo.model = StudentModel

    filters = StudentFilters(email=settings.role.admin_email)
    existing_admin = await student_repo.fetch(filters)

    if len(existing_admin.items) == 0:
        hashed_password = Hasher.get_password_hash(settings.role.admin_password)

        admin = StudentModel(
            email=settings.role.admin_email,
            first_name=settings.role.admin_first_name,
            last_name=settings.role.admin_last_name,
            hashed_password=hashed_password,
            skills=settings.role.admin_skills,
            role=settings.role.admin_role_code,
        )
        admin = await student_repo.save(admin)
        print(f'✓ Created admin user: {admin.email}')
    else:
        print(f'✓ Admin user already exists: {existing_admin.items[0].email}')


async def main() -> None:
    if settings.role.bootstrap_enabled:
        async with AsyncSession(engine) as session:
            await create_admin_user(session)


if __name__ == '__main__':
    asyncio.run(main())
