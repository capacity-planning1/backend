from enum import Enum

from sqlmodel import Field, SQLModel

from app.models.base import BaseModel


class WeekDay(str, Enum):
    MONDAY = 'Понедельник'
    TUESDAY = 'Вторник'
    WEDNESDAY = 'Среда'
    THURSDAY = 'Четверг'
    FRIDAY = 'Пятница'
    SATURDAY = 'Суббота'
    SUNDAY = 'Воскресенье'


class ScheduleBase(SQLModel):
    day: WeekDay = Field(nullable=False, max_length=50)
    time_slot: str = Field(nullable=False, max_length=50)
    group: str = Field(index=True, nullable=False, max_length=16)
    lesson_details: str = Field(nullable=False)


class ScheduleModel(BaseModel, ScheduleBase, table=True):
    __tablename__ = 'itis_schedule'
