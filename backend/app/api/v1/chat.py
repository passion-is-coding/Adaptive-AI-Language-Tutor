from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.llm.gemini import GeminiProvider
from app.schemas.chat import ChatRequest, ChatResponse
from app.tutor.analyzer import StudentAnalyzer
from app.tutor.service import TutorService


router = APIRouter(prefix="/chat", tags=["Chat"])


def get_tutor_service(
    settings: Settings = Depends(get_settings),
) -> TutorService:

    llm = GeminiProvider(settings)
    analyzer = StudentAnalyzer()

    return TutorService(
        llm=llm,
        analyzer=analyzer,
    )


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    tutor: TutorService = Depends(get_tutor_service),
) -> ChatResponse:

    return await tutor.chat(
        user_id=request.user_id,
        message=request.message,
    )