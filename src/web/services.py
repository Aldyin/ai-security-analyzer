from src.api.analyzer import (
    analyze_code
)


def analyze_service(code: str):

    result = analyze_code(code)

    return result