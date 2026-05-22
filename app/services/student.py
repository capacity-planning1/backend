from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import (
    StudentRepository,
    StudentRepositoryDep,
)
from app.models.students.student import (
    StudentCreate,
    StudentModel,
    StudentPublic,
    StudentUpdate,
)
from app.schemas.students import StudentFilters
from app.utils.hasher import Hasher


class StudentService:
    __student_repository: StudentRepository

    def __init__(self, student_repository: StudentRepositoryDep):
        self.__student_repository = student_repository

    async def get_students(self, filters: StudentFilters) -> Sequence[StudentPublic]:
        return await self.__student_repository.fetch(filters)

    async def create_student(self, student_create: StudentCreate) -> StudentPublic:
        student_dump = student_create.model_dump()
        student_dump['hashed_password'] = Hasher.get_password_hash(
            student_dump.pop('password')
        )
        student = StudentModel(**student_dump)
        return await self.__student_repository.save(student)

    async def get_student(self, student_id: UUID) -> Optional[StudentPublic]:
        return await self.__student_repository.get(student_id)

    async def update_student(
        self, student_update: StudentUpdate, student_id: UUID
    ) -> Optional[StudentPublic]:
        return await self.__student_repository.update(student_id, student_update)

    async def delete_student(self, student_id: UUID) -> Optional[StudentPublic]:
        return await self.__student_repository.delete(student_id)

    async def get_student_by_email(self, email: str) -> Optional[StudentPublic]:
        filters = StudentFilters()
        filters.email = email

        students = await self.__student_repository.fetch(filters)

        if len(students) == 0:
            return None

        return students[0]
