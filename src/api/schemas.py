from dataclasses import dataclass


@dataclass
class AnalysisResponse:

    language: str

    vulnerability: str

    confidence: float

    risk: str

    explanation: str

    fixed_code: str

    message: str