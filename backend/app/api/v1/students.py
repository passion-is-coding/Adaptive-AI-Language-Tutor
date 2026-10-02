import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student_service import StudentService


router = APIRouter(
    prefix="/students",
    tags=["Students"],
)

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    data: StudentCreate,
    db: DbSession,
):
    service = StudentService(db)
    return await service.create_student(data)


@router.get(
    "/{user_id}",
    response_model=StudentResponse,
)
async def get_student(
    user_id: uuid.UUID,
    db: DbSession,
):
    service = StudentService(db)
    return await service.get_student(user_id)