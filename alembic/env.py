# alembic/env.py
import asyncio  # Добавили для запуска асинхронного цикла
from logging.config import fileConfig
from sqlalchemy import pool  # Убрали engine_from_config, он больше не нужен
from alembic import context
from sqlmodel import SQLModel
import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import async_engine_from_config  # Используем его

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent.parent))

from app.models.students.student import StudentModel
from app.models.projects.project import ProjectModel
from app.models.auth.refresh_session import RefreshSessionModel
from app.models.projects.project_member import ProjectMemberModel
from app.models.projects.team import TeamModel
from app.models.projects.team_membership import TeamMembershipModel
from app.models.sprints.sprint import SprintModel
from app.models.sprints.sprint_task import SprintTaskModel
from app.models.sprints.task_assignment import TaskAssignmentModel
from app.models.sprints.task_change_request import TaskChangeRequestModel
from app.models.students.busy_slot import BusySlotModel
# Импортируем настройки
from app.core.config import settings

# Alembic Config object
config = context.config

# КЛЮЧЕВОЕ: берем URL из настроек и заменяем asyncpg на psycopg2
database_url = str(settings.database_url)
config.set_main_option("sqlalchemy.url", database_url)

print(database_url)

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для autogenerate
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    """Вспомогательная функция для синхронного выполнения миграций внутри асинхронного соединения."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode (исправлено на асинхронный)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    # Запускаем асинхронную функцию через asyncio
    asyncio.run(run_migrations_online())