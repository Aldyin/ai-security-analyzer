from src.api.analyzer import (
    analyze_code
)


def auto_analyze(code):

    result = analyze_code(code)

    return {
        "language": result.language,
        "vulnerability": result.vulnerability,
        "confidence": result.confidence,
        "risk": result.risk,
        "explanation": result.explanation,
        "fixed_code": result.fixed_code,
        "message": result.message
    }