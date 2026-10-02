import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student_profile import StudentProfile
from app.models.user import User
from app.schemas.student import StudentCreate


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        data: StudentCreate,
    ) -> StudentProfile:
        user = User(
            email=str(data.email) if data.email else None,
            auth_provider=data.auth_provider,
            auth_subject=data.auth_subject,
        )

        profile = StudentProfile(
            user=user,
            cefr_level=data.cefr_level,
            learning_goal=data.learning_goal,
        )

        self.db.add(user)
        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def get_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> StudentProfile | None:
        result = await self.db.execute(
            select(StudentProfile).where(
                StudentProfile.user_id == user_id
            )
        )
        return result.scalar_one_or_none()