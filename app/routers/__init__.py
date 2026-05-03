from app.routers.projects.projects import router as projects
from app.routers.sprints.sprints import router as sprints
from app.routers.students.students import router as students
from app.routers.auth.auth import router as auth
from app.routers.roles.roles import router as roles

__all__ = ['projects', 'sprints', 'students', 'auth', 'roles']