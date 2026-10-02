import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate, StudentResponse


class StudentService:
    def __init__(self, db: AsyncSession):
        self.repository = StudentRepository(db)

    async def create_student(
        self,
        data: StudentCreate,
    ) -> StudentResponse:
        if data.cefr_level not in {
            "A1", "A2", "B1", "B2", "C1", "C2"
        }:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid CEFR level",
            )

        profile = await self.repository.create(data)

        return StudentResponse.model_validate(profile)

    async def get_student(
        self,
        user_id: uuid.UUID,
    ) -> StudentResponse:
        profile = await self.repository.get_by_user_id(user_id)

        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )

        return StudentResponse.model_validate(profile)