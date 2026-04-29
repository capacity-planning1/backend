from typing import Annotated, TypeAlias, TYPE_CHECKING

from fastapi import Depends

from app.utils.repository import Repository

if TYPE_CHECKING:
    from app.dependencies.session import SessionDep
    from app.models.projects.project import ProjectModel
    from app.models.projects.project_member import ProjectMemberModel
    from app.models.projects.team import TeamModel
    from app.models.projects.team_membership import TeamMembershipModel

    from app.models.sprints.sprint import SprintModel
    from app.models.sprints.sprint_task import SprintTaskModel
    from app.models.sprints.task_assignment import TaskAssignmentModel
    from app.models.sprints.task_change_request import TaskChangeRequestModel

    from app.models.students.student import StudentModel
    from app.models.students.busy_slot import BusySlotModel

    from app.models.token_blacklist import TokenBlacklistModel
    from app.repositories.token_blacklist import TokenBlacklistRepository


async def get_project_repository(session: SessionDep):
    yield Repository[ProjectModel](session)


ProjectRepository: TypeAlias = Repository[ProjectModel]
ProjectRepositoryDep = Annotated[ProjectRepository, Depends(get_project_repository)]


async def get_project_member_repository(session: SessionDep):
    yield Repository[ProjectMemberModel](session)


ProjectMemberRepository: TypeAlias = Repository[ProjectMemberModel]
ProjectMemberRepositoryDep = Annotated[
    ProjectMemberRepository, Depends(get_project_member_repository)
]


async def get_team_repository(session: SessionDep):
    yield Repository[TeamModel](session)


TeamRepository: TypeAlias = Repository[TeamModel]
TeamRepositoryDep = Annotated[TeamRepository, Depends(get_team_repository)]


async def get_team_membership_repository(session: SessionDep):
    yield Repository[TeamMembershipModel](session)


TeamMembershipRepository: TypeAlias = Repository[TeamMembershipModel]
TeamMembershipRepositoryDep = Annotated[
    TeamMembershipRepository, Depends(get_team_membership_repository)
]


async def get_task_assignment_repository(session: SessionDep):
    yield Repository[TaskAssignmentModel](session)


TaskAssignmentRepository: TypeAlias = Repository[TaskAssignmentModel]
TaskAssignmentRepositoryDep = Annotated[
    TaskAssignmentRepository, Depends(get_task_assignment_repository)
]


async def get_task_change_request_repository(session: SessionDep):
    yield Repository[TaskChangeRequestModel](session)


TaskChangeRequestRepository: TypeAlias = Repository[TaskChangeRequestModel]
TaskChangeRequestRepositoryDep = Annotated[
    TaskChangeRequestRepository, Depends(get_task_change_request_repository)
]


async def get_sprint_repository(session: SessionDep):
    yield Repository[SprintModel](session)


SprintRepository: TypeAlias = Repository[SprintModel]
SprintRepositoryDep = Annotated[SprintRepository, Depends(get_sprint_repository)]


async def get_sprint_task_repository(session: SessionDep):
    yield Repository[SprintTaskModel](session)


SprintTaskRepository: TypeAlias = Repository[SprintTaskModel]
SprintTaskRepositoryDep = Annotated[
    SprintTaskRepository, Depends(get_sprint_task_repository)
]


async def get_busy_slot_repository(session: SessionDep):
    yield Repository[BusySlotModel](session)


BusySlotRepository: TypeAlias = Repository[BusySlotModel]
BusySlotRepositoryDep = Annotated[BusySlotRepository, Depends(get_busy_slot_repository)]


async def get_student_repository(session: SessionDep):
    yield Repository[StudentModel](session)


StudentRepository: TypeAlias = Repository[StudentModel]
StudentRepositoryDep = Annotated[StudentRepository, Depends(get_student_repository)]


async def get_token_blacklist_repository(session: SessionDep):
    yield TokenBlacklistRepository(session)


TokenBlacklistRepositoryDep = Annotated[TokenBlacklistRepository, Depends(get_token_blacklist_repository)]
