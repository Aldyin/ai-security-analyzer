from src.core.exceptions import (
    InvalidCodeError
)


def validate_code(code: str):

    if not code:
        raise InvalidCodeError(
            "Code is empty"
        )

    if not code.strip():
        raise InvalidCodeError(
            "Code contains only whitespace"
        )

    if len(code) < 3:
        raise InvalidCodeError(
            "Code is too short"
        )

    return True