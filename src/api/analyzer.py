from src.logging.logger import (
    get_logger
)

from src.api.validators import (
    validate_code
)

from src.api.responses import (
    build_response
)

from src.application.use_cases.predict_language import (
    predict_language
)

from src.application.use_cases.predict_vulnerability import (
    predict_vulnerability
)

from src.security.rules import (
    calculate_risk
)

from src.remediation.explanations import (
    generate_explanation
)

from src.remediation.fixer import (
    generate_fix
)


logger = get_logger(
    "analyzer"
)


def analyze_code(code: str):

    logger.info(
        "Starting analysis"
    )

    validate_code(code)

    # ==========================================
    # LANGUAGE
    # ==========================================

    language = predict_language(
        code
    )

    logger.info(
        f"Detected language: {language}"
    )

    # ==========================================
    # VULNERABILITY
    # ==========================================

    vulnerability, confidence = (
        predict_vulnerability(code)
    )

    logger.info(
        f"Detected vulnerability: {vulnerability}"
    )

    # ==========================================
    # RISK
    # ==========================================

    risk = calculate_risk(
        vulnerability,
        confidence
    )

    # ==========================================
    # EXPLANATION
    # ==========================================

    explanation = generate_explanation(
        vulnerability
    )

    # ==========================================
    # FIX
    # ==========================================

    fixed_code = generate_fix(
        vulnerability,
        code
    )

    # ==========================================
    # MESSAGE
    # ==========================================

    if vulnerability == "SAFE":

        message = (
            "No vulnerabilities detected"
        )

    else:

        message = (
            f"{vulnerability} detected"
        )

    logger.info(
        "Analysis completed"
    )

    return build_response(
        language=language,
        vulnerability=vulnerability,
        confidence=round(
            confidence * 100,
            2
        ),
        risk=risk,
        explanation=explanation,
        fixed_code=fixed_code,
        message=message
    )