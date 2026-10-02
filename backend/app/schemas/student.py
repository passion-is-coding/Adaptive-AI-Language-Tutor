import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    email: EmailStr | None = None
    auth_provider: str = "local"
    auth_subject: str | None = None
    cefr_level: str = "B1"
    learning_goal: str | None = Field(
        default=None,
        max_length=500,
    )


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    cefr_level: str
    learning_goal: str | None
    preferences: dict
    created_at: datetime
    updated_at: datetime