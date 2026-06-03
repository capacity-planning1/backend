import json
import os
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

TESTS_DIR = Path(__file__).parent
FIXTURES_DIR = TESTS_DIR / 'fixtures'
TEST_RUNTIME_DIR = Path('.pytest_cache')
TEST_RUNTIME_DIR.mkdir(exist_ok=True)

TEST_DATABASE_URL = f'sqlite+aiosqlite:///{TEST_RUNTIME_DIR / "test.sqlite"}'

os.environ.setdefault('DB__DATABASE_ECHO', 'False')
os.environ.setdefault('AUTH__ALGORITHM', 'HS256')
os.environ.setdefault('AUTH__PRIVATE_KEY_PATH', str(FIXTURES_DIR / 'auth_private.txt'))
os.environ.setdefault('AUTH__PUBLIC_KEY_PATH', str(FIXTURES_DIR / 'auth_public.txt'))
os.environ.setdefault('COMMON__BACKEND_HOST', 'http://testserver')
os.environ.setdefault('COMMON__FRONTEND_HOST', 'http://frontend.test')
os.environ.setdefault('ROLE__ADMIN_EMAIL', 'admin@example.com')
os.environ.setdefault('ROLE__ADMIN_PASSWORD', 'Admin123!')
os.environ.setdefault('ROLE__ADMIN_FIRST_NAME', 'Admin')
os.environ.setdefault('ROLE__ADMIN_LAST_NAME', 'User')
os.environ.setdefault('ROLE__ADMIN_SKILLS', 'System Admin')
os.environ.setdefault('ROLE__ADMIN_ROLE_CODE', 'admin')
os.environ.setdefault('ROLE__DEFAULT_USER_ROLE_CODE', 'user')
os.environ.setdefault('ROLE__BOOTSTRAP_ENABLED', 'false')
os.environ.setdefault('LIMITER__DEFAULT_LIMITS', '["1000/minute"]')
os.environ.setdefault('LOGGING__FILE_NAME', str(TEST_RUNTIME_DIR / 'test.log'))
os.environ.setdefault('EMAIL__USERNAME', 'test@example.com')
os.environ.setdefault('EMAIL__PASSWORD', 'test-password')
os.environ.setdefault('EMAIL__TEMPLATES_DIR', str(FIXTURES_DIR))

from app.dependencies.session import get_session  # noqa: E402
from app.main import app  # noqa: E402
from app.models import *  # noqa: F403, E402
from app.services.email import EmailService  # noqa: E402

app.root_path = ''

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_test_session() -> AsyncIterator[AsyncSession]:
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


def _deduplicate_sqlite_indexes() -> None:
    for table in SQLModel.metadata.tables.values():
        seen_indexes = set()
        duplicated_indexes = []

        for index in table.indexes:
            if index.name in seen_indexes:
                duplicated_indexes.append(index)
            else:
                seen_indexes.add(index.name)

        for index in duplicated_indexes:
            table.indexes.remove(index)


@pytest.fixture(autouse=True)
async def reset_database() -> AsyncIterator[None]:
    _deduplicate_sqlite_indexes()

    async with test_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(autouse=True)
def disable_email_delivery(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        EmailService,
        'send_verification_email',
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        EmailService,
        'send_change_password_email',
        lambda *args, **kwargs: None,
    )


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url='http://testserver',
    ) as test_client:
        yield test_client


@pytest.fixture
def load_fixture() -> Any:
    def _load_fixture(file_name: str) -> Any:
        fixture_path = FIXTURES_DIR / file_name
        return json.loads(fixture_path.read_text(encoding='utf-8'))

    return _load_fixture
