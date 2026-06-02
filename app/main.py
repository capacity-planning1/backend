from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware

from app.core.config import settings
from app.core.error_handler import exception_handler
from app.core.limiter import limiter
from app.core.middlewares import request_logging_middleware
from app.core.responses import GLOBAL_RESPONSES
from app.routers import auth, projects, roles, sprints, students

app = FastAPI(
    title='Capacity Planning API',
    version='1.0.0',
    responses=GLOBAL_RESPONSES,
    root_path="/api",
)

api_prefix = '/api'

origins = ['http://localhost:8080']

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=exception_handler
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['Authorization', 'Content-Type', 'X-Requested-With', 'user-agent'],
    max_age=3600,
)
app.add_middleware(SlowAPIASGIMiddleware)
app.middleware('http')(request_logging_middleware)

app_router = APIRouter(prefix=f'{api_prefix}/v1')
app_router.include_router(projects)
app_router.include_router(sprints)
app_router.include_router(students)
app_router.include_router(auth)
app_router.include_router(roles)

app.include_router(app_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title='Capacity Planning API',
        version='1.1.0',
        description='API for planning tasks in students projects',
        routes=app.routes,
        servers=[
            {
                'url': settings.common.backend_host,
                'description': 'Local server',
            },
        ],
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
