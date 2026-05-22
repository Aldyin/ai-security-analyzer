from src.remediation.fix_templates import FIX_TEMPLATES


def get_explanation(vulnerability: str):

    if vulnerability not in FIX_TEMPLATES:
        return "No explanation available."

    return FIX_TEMPLATES[vulnerability]["explanation"]


def get_risk_level(vulnerability: str):

    if vulnerability not in FIX_TEMPLATES:
        return "UNKNOWN"

    return FIX_TEMPLATES[vulnerability]["risk"]