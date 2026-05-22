from src.api.schemas import (
    AnalysisResponse
)


def build_response(
    language,
    vulnerability,
    confidence,
    risk,
    explanation,
    fixed_code,
    message
):

    return AnalysisResponse(
        language=language,
        vulnerability=vulnerability,
        confidence=confidence,
        risk=risk,
        explanation=explanation,
        fixed_code=fixed_code,
        message=message
    )