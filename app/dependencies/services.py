from typing import Annotated

from fastapi.params import Depends

from app.services.busy_slot import BusySlotService
from app.services.project import ProjectService
from app.services.project_member import ProjectMemberService
from app.services.sprint import SprintService
from app.services.sprint_task import SprintTaskService
from app.services.student import StudentService
from app.services.task_assignment import TaskAssignmentService
from app.services.task_change_request import TaskChangeRequestService
from app.services.team import TeamService
from app.services.team_membership import TeamMembershipService
from app.services.refresh_session import RefreshSessionService

BusySlotServiceDep = Annotated[BusySlotService, Depends(BusySlotService)]

StudentServiceDep = Annotated[StudentService, Depends(StudentService)]

ProjectServiceDep = Annotated[ProjectService, Depends(ProjectService)]

ProjectMemberServiceDep = Annotated[ProjectMemberService, Depends(ProjectMemberService)]

TeamServiceDep = Annotated[TeamService, Depends(TeamService)]

TeamMembershipServiceDep = Annotated[
    TeamMembershipService, Depends(TeamMembershipService)
]

SprintServiceDep = Annotated[SprintService, Depends(SprintService)]

SprintTaskServiceDep = Annotated[SprintTaskService, Depends(SprintTaskService)]

TaskAssignmentServiceDep = Annotated[
    TaskAssignmentService, Depends(TaskAssignmentService)
]

TaskChangeRequestServiceDep = Annotated[
    TaskChangeRequestService, Depends(TaskChangeRequestService)
]

RefreshSessionServiceDep = Annotated[RefreshSessionService, Depends(RefreshSessionService)]
