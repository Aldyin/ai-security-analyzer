from fastapi import APIRouter

from src.web.schemas import (
    AnalyzeRequest,
    AnalyzeResponse
)

from src.web.services import (
    analyze_service
)


router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze(
    request: AnalyzeRequest
):

    result = analyze_service(
        request.code
    )

    return result