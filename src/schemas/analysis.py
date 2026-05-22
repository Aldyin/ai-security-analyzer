from dataclasses import dataclass


@dataclass
class AnalysisResult:

    language: str

    vulnerability: str

    confidence: float

    risk: str

    explanation: str

    fixed_code: str