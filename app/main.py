from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware

from app.core.limiter import limiter
from app.routers import auth, projects, roles, sprints, students

app = FastAPI(
    title='Capacity Planning API',
    version='1.0.0',
)

api_prefix = '/api'

origins = ['http://localhost:8080']

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIASGIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['Authorization', 'Content-Type', 'X-Requested-With', 'user-agent'],
    max_age=3600,
)

app_router = APIRouter(prefix=f'{api_prefix}/v1')
app_router.include_router(projects)
app_router.include_router(sprints)
app_router.include_router(students)
app_router.include_router(auth)
app_router.include_router(roles)

app.include_router(app_router)
