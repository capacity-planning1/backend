from app.routers.auth import router as auth
from app.routers.projects.projects import router as projects
from app.routers.roles import router as roles
from app.routers.sprints.sprints import router as sprints
from app.routers.students.students import router as students

__all__ = ['projects', 'sprints', 'students', 'auth', 'roles']
