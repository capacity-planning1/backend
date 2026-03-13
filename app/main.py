from contextlib import asynccontextmanager
from datetime import date, datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlmodel import Session, select

from app import models
from app.database import create_db_and_tables, get_session
from app.models import Project, ProjectMember, Student, Team, TeamMembership


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Capacity Planning API",
    version="1.0.0",
    lifespan=lifespan,
)


def paginate(statement, session: Session, page: int, page_size: int):
    total = len(session.exec(statement).all())
    items = session.exec(
        statement.offset((page - 1) * page_size).limit(page_size)
    ).all()
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def get_student_or_404(session: Session, student_id: int) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def get_project_or_404(session: Session, project_id: int) -> Project:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def get_team_or_404(session: Session, team_id: int) -> Team:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


def get_project_member_by_project_and_student_or_404(
    session: Session, project_id: int, student_id: int
) -> ProjectMember:
    statement = select(ProjectMember).where(
        ProjectMember.project_id == project_id,
        ProjectMember.student_id == student_id,
    )
    project_member = session.exec(statement).first()
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")
    return project_member


def get_team_membership_by_team_and_project_member_or_404(
    session: Session, team_id: int, project_member_id: int
) -> TeamMembership:
    statement = select(TeamMembership).where(
        TeamMembership.team_id == team_id,
        TeamMembership.project_member_id == project_member_id,
    )
    membership = session.exec(statement).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Team membership not found")
    return membership


@app.get("/")
def read_root():
    return {"message": "Capacity Planning API is running"}


@app.get("/students/profile")
def get_current_student_profile(session: Session = Depends(get_session)):
    """
    Временная заглушка вместо авторизации.
    Возвращает первого студента из БД.
    """
    student = session.exec(select(Student)).first()
    if not student:
        raise HTTPException(status_code=404, detail="No students found")
    return student


@app.get("/students")
def get_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    skills: Optional[str] = None,
    session: Session = Depends(get_session),
):
    statement = select(Student)

    if email:
        statement = statement.where(Student.email.contains(email))
    if first_name:
        statement = statement.where(Student.first_name.contains(first_name))
    if last_name:
        statement = statement.where(Student.last_name.contains(last_name))
    if skills:
        statement = statement.where(Student.skills.contains(skills))

    return paginate(statement, session, page, page_size)


@app.get("/students/{student_id}")
def get_student(student_id: int, session: Session = Depends(get_session)):
    return get_student_or_404(session, student_id)


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student_data: Student,
    session: Session = Depends(get_session),
):
    student = get_student_or_404(session, student_id)

    student.email = student_data.email
    student.first_name = student_data.first_name
    student.last_name = student_data.last_name
    student.skills = student_data.skills

    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = get_student_or_404(session, student_id)
    session.delete(student)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/projects")
def get_projects(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    name: Optional[str] = None,
    owner_student_id: Optional[int] = Query(default=None, ge=1),
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    session: Session = Depends(get_session),
):
    statement = select(Project)

    if name:
        statement = statement.where(Project.name.contains(name))
    if owner_student_id:
        statement = statement.where(Project.owner_student_id == owner_student_id)
    if created_from:
        statement = statement.where(Project.created_at >= created_from)
    if created_to:
        statement = statement.where(Project.created_at <= created_to)

    return paginate(statement, session, page, page_size)


@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project_data: Project, session: Session = Depends(get_session)):
    get_student_or_404(session, project_data.owner_student_id)

    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_student_id=project_data.owner_student_id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.post("/projects/join", status_code=status.HTTP_201_CREATED)
def join_project(
    join_data: ProjectMember,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, join_data.project_id)
    get_student_or_404(session, join_data.student_id)

    existing = session.exec(
        select(ProjectMember).where(
            ProjectMember.project_id == join_data.project_id,
            ProjectMember.student_id == join_data.student_id,
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Student already joined this project")

    project_member = ProjectMember(
        project_id=join_data.project_id,
        student_id=join_data.student_id,
        role=join_data.role,
        is_active=join_data.is_active,
    )
    session.add(project_member)
    session.commit()
    session.refresh(project_member)
    return project_member


@app.get("/projects/{project_id}")
def get_project(project_id: int, session: Session = Depends(get_session)):
    return get_project_or_404(session, project_id)


@app.put("/projects/{project_id}")
def update_project(
    project_id: int,
    project_data: Project,
    session: Session = Depends(get_session),
):
    project = get_project_or_404(session, project_id)

    project.name = project_data.name
    project.description = project_data.description
    project.owner_student_id = project_data.owner_student_id

    get_student_or_404(session, project.owner_student_id)

    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = get_project_or_404(session, project_id)
    session.delete(project)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/projects/{project_id}/members")
def get_project_members(
    project_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    student_id: Optional[int] = Query(default=None, ge=1),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    join_date_from: Optional[date] = None,
    join_date_to: Optional[date] = None,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)

    statement = select(ProjectMember).where(ProjectMember.project_id == project_id)

    if student_id:
        statement = statement.where(ProjectMember.student_id == student_id)
    if role:
        statement = statement.where(ProjectMember.role.contains(role))
    if is_active is not None:
        statement = statement.where(ProjectMember.is_active == is_active)
    if join_date_from:
        statement = statement.where(ProjectMember.join_date >= join_date_from)
    if join_date_to:
        statement = statement.where(ProjectMember.join_date <= join_date_to)

    return paginate(statement, session, page, page_size)


@app.post("/projects/{project_id}/members", status_code=status.HTTP_201_CREATED)
def add_project_member(
    project_id: int,
    member_data: ProjectMember,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    get_student_or_404(session, member_data.student_id)

    existing = session.exec(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.student_id == member_data.student_id,
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Student already in project")

    project_member = ProjectMember(
        project_id=project_id,
        student_id=member_data.student_id,
        role=member_data.role,
        is_active=member_data.is_active,
    )
    session.add(project_member)
    session.commit()
    session.refresh(project_member)
    return project_member


@app.get("/projects/{project_id}/members/{student_id}")
def get_project_member(
    project_id: int,
    student_id: int,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    return get_project_member_by_project_and_student_or_404(
        session, project_id, student_id
    )


@app.put("/projects/{project_id}/members/{student_id}")
def update_project_member(
    project_id: int,
    student_id: int,
    member_data: ProjectMember,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    project_member = get_project_member_by_project_and_student_or_404(
        session, project_id, student_id
    )

    project_member.role = member_data.role
    project_member.is_active = member_data.is_active

    session.add(project_member)
    session.commit()
    session.refresh(project_member)
    return project_member


@app.delete(
    "/projects/{project_id}/members/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_member(
    project_id: int,
    student_id: int,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    project_member = get_project_member_by_project_and_student_or_404(
        session, project_id, student_id
    )
    session.delete(project_member)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/projects/{project_id}/teams")
def get_teams(
    project_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)

    statement = select(Team).where(Team.project_id == project_id)
    return paginate(statement, session, page, page_size)


@app.post("/projects/{project_id}/teams", status_code=status.HTTP_201_CREATED)
def create_team(
    project_id: int,
    team_data: Team,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)

    team = Team(
        project_id=project_id,
        name=team_data.name,
        description=team_data.description,
    )
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@app.get("/projects/{project_id}/teams/{team_id}")
def get_team(
    project_id: int,
    team_id: int,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    team = get_team_or_404(session, team_id)

    if team.project_id != project_id:
        raise HTTPException(status_code=404, detail="Team not found in this project")

    return team


@app.put("/projects/{project_id}/teams/{team_id}")
def update_team(
    project_id: int,
    team_id: int,
    team_data: Team,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    team = get_team_or_404(session, team_id)

    if team.project_id != project_id:
        raise HTTPException(status_code=404, detail="Team not found in this project")

    team.name = team_data.name
    team.description = team_data.description

    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@app.delete("/projects/{project_id}/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    project_id: int,
    team_id: int,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    team = get_team_or_404(session, team_id)

    if team.project_id != project_id:
        raise HTTPException(status_code=404, detail="Team not found in this project")

    session.delete(team)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/projects/{project_id}/teams/{team_id}/members")
def get_team_members(
    project_id: int,
    team_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    team = get_team_or_404(session, team_id)

    if team.project_id != project_id:
        raise HTTPException(status_code=404, detail="Team not found in this project")

    statement = select(TeamMembership).where(TeamMembership.team_id == team_id)
    return paginate(statement, session, page, page_size)


@app.post("/projects/{project_id}/teams/{team_id}/members", status_code=status.HTTP_201_CREATED)
def add_team_member(
    project_id: int,
    team_id: int,
    membership_data: TeamMembership,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    team = get_team_or_404(session, team_id)

    if team.project_id != project_id:
        raise HTTPException(status_code=404, detail="Team not found in this project")

    project_member = session.get(ProjectMember, membership_data.project_member_id)
    if not project_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    if project_member.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Project member does not belong to this project",
        )

    existing = session.exec(
        select(TeamMembership).where(
            TeamMembership.team_id == team_id,
            TeamMembership.project_member_id == membership_data.project_member_id,
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Member already in team")

    membership = TeamMembership(
        team_id=team_id,
        project_member_id=membership_data.project_member_id,
        position=membership_data.position,
    )
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership


@app.put("/projects/{project_id}/teams/{team_id}/members/{student_id}")
def update_team_member(
    project_id: int,
    team_id: int,
    student_id: int,
    membership_data: TeamMembership,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    team = get_team_or_404(session, team_id)

    if team.project_id != project_id:
        raise HTTPException(status_code=404, detail="Team not found in this project")

    project_member = get_project_member_by_project_and_student_or_404(
        session, project_id, student_id
    )
    membership = get_team_membership_by_team_and_project_member_or_404(
        session, team_id, project_member.id
    )

    membership.position = membership_data.position

    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership


@app.delete(
    "/projects/{project_id}/teams/{team_id}/members/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_team_member(
    project_id: int,
    team_id: int,
    student_id: int,
    session: Session = Depends(get_session),
):
    get_project_or_404(session, project_id)
    team = get_team_or_404(session, team_id)

    if team.project_id != project_id:
        raise HTTPException(status_code=404, detail="Team not found in this project")

    project_member = get_project_member_by_project_and_student_or_404(
        session, project_id, student_id
    )
    membership = get_team_membership_by_team_and_project_member_or_404(
        session, team_id, project_member.id
    )

    session.delete(membership)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)