from contextlib import asynccontextmanager

from app.db.database import engine
from fastapi import APIRouter, FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bootstrap import create_admin_user
from app.core.config import settings
from app.routers import auth, projects, roles, sprints, students

from app.models.auth.refresh_session import RefreshSessionModel
from app.models.projects.project import ProjectModel
from app.models.projects.project_member import ProjectMemberModel
from app.models.projects.team import TeamModel
from app.models.projects.team_membership import TeamMembershipModel
from app.models.sprints.sprint import SprintModel
from app.models.sprints.sprint_task import SprintTaskModel
from app.models.sprints.task_assignment import TaskAssignmentModel
from app.models.sprints.task_change_request import TaskChangeRequestModel
from app.models.students.busy_slot import BusySlotModel
from app.models.students.student import StudentModel

@asynccontextmanager
async def lifespan(_app: FastAPI):
    if settings.bootstrap_enabled:
        async with AsyncSession(engine) as session:
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
