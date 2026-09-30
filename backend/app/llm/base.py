from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMRequest:
    system_instruction: str
    user_message: str


@dataclass
class LLMResponse:
    text: str
    model: str


class LLMProvider(ABC):

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError