from datetime import date, datetime, timedelta
from uuid import UUID

from sqlmodel import select

from app.dependencies.repositories import BusySlotRepositoryDep
from app.dependencies.session import SessionDep
from app.models.students.busy_slot import BusySlotModel, SlotType
from app.models.schedule import WeekDay, ScheduleModel

WEEKDAY_TO_NUM ={
    WeekDay.MONDAY: 0,
    WeekDay.TUESDAY: 1,
    WeekDay.WEDNESDAY: 2,
    WeekDay.THURSDAY: 3,
    WeekDay.FRIDAY: 4,
    WeekDay.SATURDAY: 5,
    WeekDay.SUNDAY:6,
}

class ScheduleService:
    def __init__(
        self, busy_slot_repo: BusySlotRepositoryDep, session: SessionDep
    ):
        self.__session = session
        self.__busy_slot_repo = busy_slot_repo

    async def fill_student_schedule(self, student_id: UUID, group_name: str) -> None:
        statement = select(ScheduleModel).where(ScheduleModel.group == group_name.strip())

        result = await self.__session.exec(statement)
        lessons = result.all()
        if not lessons:
            return

        start_semester = date(2026, 2, 9)
        end_semester = date(2026, 6, 30)
        current_date = start_semester

        slots_to_create = []

        while current_date <= end_semester:
            weekday_num = current_date.weekday()

            for lesson in lessons:
                if WEEKDAY_TO_NUM.get(lesson.day) == weekday_num:
                    try:
                        clean_time_range = lesson.time_slot.replace(" ", "")
                        start_str, end_str = clean_time_range.split('-')
                        start_h, start_m = map(int, start_str.split('.'))
                        end_h, end_m = map(int, end_str.split('.'))

                        start_dt = datetime.combine(current_date, datetime.min.time()).replace(hour=start_h, minute=start_m)
                        end_dt = datetime.combine(current_date, datetime.min.time()).replace(hour=end_h, minute=end_m)

                        new_slot = BusySlotModel(
                            student_id=student_id,
                            slot_type=SlotType.PAIR,
                            start_datetime=start_dt,
                            end_datetime=end_dt,
                            description=lesson.lesson_details,
                            task_assignment_id=None
                        )
                        slots_to_create.append(new_slot)

                    except ValueError:
                        continue

            current_date += timedelta(days=1)
        if slots_to_create:
            await self.__busy_slot_repo.create_many(slots_to_create)
