from google import genai
from google.genai import types

from app.core.config import Settings
from app.llm.base import LLMProvider, LLMRequest, LLMResponse


class GeminiProvider(LLMProvider):
    def __init__(self, settings: Settings):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    async def generate(self, request: LLMRequest) -> LLMResponse:

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=request.user_message,
            config=types.GenerateContentConfig(
                system_instruction=request.system_instruction,
                temperature=0.7,
            ),
        )

        return LLMResponse(
            text=response.text or "",
            model=self.model,
        )
