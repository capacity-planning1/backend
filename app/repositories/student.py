from typing import Optional

from sqlmodel import select

from app.models.students.student import StudentModel
from app.utils.repository import Repository


class StudentRepository(Repository[StudentModel]):
    async def get_by_email(self, email: str) -> Optional[StudentModel]:
        statement = select(self.model).where(self.model.email == email)

        result = await self._session.exec(statement)
        return result.first()
