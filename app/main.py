from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.core.config import settings
from app.routers import projects, sprints, students, auth, roles
from app.bootstrap import bootstrap_roles_permissions, create_admin_user 

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.bootstrap_enabled:
        async with AsyncSession(engine) as session:
            await bootstrap_roles_permissions(session)
            await create_admin_user(session)

    yield


app = FastAPI(
    title='Capacity Planning API',
    version='1.0.0',
    lifespan=lifespan,
)

api_prefix = '/api'

app_router = APIRouter(prefix=f'{api_prefix}/v1')
app_router.include_router(projects)
app_router.include_router(sprints)
app_router.include_router(students)
app_router.include_router(auth)
app_router.include_router(roles)

app.include_router(app_router)
