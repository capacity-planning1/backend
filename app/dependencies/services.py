from typing import Annotated

from fastapi.params import Depends

from app.services.projects import (
    ProjectMemberService,
    ProjectService,
    TeamService,
    TeamMembershipService,
)
from app.services.sprints import (
    SprintService,
    SprintTaskService,
    TaskAssignmentService,
    TaskChangeRequestService,
)
from app.services.students import BusySlotService, StudentService

BusySlotServiceDep = Annotated[BusySlotService, Depends(BusySlotService)]

StudentServiceDep = Annotated[StudentService, Depends(StudentService)]

ProjectServiceDep = Annotated[ProjectService, Depends(ProjectService)]

ProjectMemberServiceDep = Annotated[
    ProjectMemberService, Depends(ProjectMemberService)
]

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
