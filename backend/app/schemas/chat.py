from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1)
    message: str = Field(min_length=1, max_length=5000)


class AdaptiveMetrics(BaseModel):
    word_count: int
    response_length: str
    suggest_expansion: bool
    target_complexity: str


class ChatResponse(BaseModel):
    conversation_id: str
    tutor_response: str
    adaptive_metrics: AdaptiveMetrics
    model: str
