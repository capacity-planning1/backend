from fastapi import APIRouter, FastAPI

from app.routers import projects, sprints, students

app = FastAPI(
    title='Capacity Planning API',
    version='1.0.0',
)

api_prefix = '/api'

app_router = APIRouter(prefix=f'{api_prefix}/v1')
app_router.include_router(projects.router)
app_router.include_router(sprints.router)
app_router.include_router(students.router)
