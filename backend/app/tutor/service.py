from uuid import uuid4

from app.llm.base import LLMProvider, LLMRequest
from app.schemas.chat import AdaptiveMetrics, ChatResponse
from app.tutor.analyzer import StudentAnalyzer


class TutorService:
    def __init__(
        self,
        llm: LLMProvider,
        analyzer: StudentAnalyzer,
    ):
        self.llm = llm
        self.analyzer = analyzer

    async def chat(
        self,
        user_id: str,
        message: str,
        user_cefr_level: str = "B1",
    ) -> ChatResponse:

        analysis = self.analyzer.analyze(
            text=message,
            current_level=user_cefr_level,
        )

        system_instruction = f"""
You are an empathetic and professional English tutor.

Student CEFR level:
{analysis.target_complexity}

Teaching requirements:

1. Adapt vocabulary and grammar to the student's CEFR level.
2. Keep the conversation natural.
3. If the student makes an important English mistake,
   gently correct it.
4. Do not correct every tiny mistake during natural conversation.
5. Encourage the student to continue speaking.

Student response characteristics:

- Word count: {analysis.word_count}
- Response length: {analysis.response_length}
- Needs expansion: {analysis.suggest_expansion}
"""

        if analysis.suggest_expansion:
            system_instruction += """
The student's response is very short.
Encourage a longer response with an open-ended follow-up question.
"""

        llm_response = await self.llm.generate(
            LLMRequest(
                system_instruction=system_instruction,
                user_message=message,
            )
        )

        return ChatResponse(
            conversation_id=str(uuid4()),
            tutor_response=llm_response.text,
            adaptive_metrics=AdaptiveMetrics(
                word_count=analysis.word_count,
                response_length=analysis.response_length,
                suggest_expansion=analysis.suggest_expansion,
                target_complexity=analysis.target_complexity,
            ),
            model=llm_response.model,
        )
