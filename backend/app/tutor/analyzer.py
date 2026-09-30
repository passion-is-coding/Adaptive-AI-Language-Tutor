from dataclasses import dataclass


@dataclass
class StudentAnalysis:
    word_count: int
    response_length: str
    suggest_expansion: bool
    target_complexity: str


class StudentAnalyzer:

    def analyze(
        self,
        text: str,
        current_level: str,
    ) -> StudentAnalysis:

        words = text.split()
        word_count = len(words)

        if word_count <= 3:
            response_length = "very_short"
        elif word_count <= 8:
            response_length = "short"
        elif word_count <= 20:
            response_length = "medium"
        else:
            response_length = "long"

        suggest_expansion = (
            word_count < 4
            and current_level in {"B1", "B2", "C1"}
        )

        return StudentAnalysis(
            word_count=word_count,
            response_length=response_length,
            suggest_expansion=suggest_expansion,
            target_complexity=current_level,
        )