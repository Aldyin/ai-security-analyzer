from pydantic import BaseModel


class AnalyzeRequest(BaseModel):

    code: str


class AnalyzeResponse(BaseModel):

    language: dict

    vulnerability: str

    confidence: float

    risk: str

    explanation: str

    fixed_code: str

    message: str

    detection_source: str