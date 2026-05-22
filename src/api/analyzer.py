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
    detect_vulnerability_rule,
    calculate_risk
)

from src.remediation.explanations import (
    generate_explanation
)

from src.remediation.fixer import (
    generate_fix
)

from src.config import (
    CONFIDENCE_THRESHOLD
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
    # LANGUAGE DETECTION
    # ==========================================

    language = predict_language(
        code
    )

    logger.info(
        f"Detected language: {language}"
    )

    # ==========================================
    # RULE-BASED DETECTION
    # ==========================================

    rule_vulnerability = (
        detect_vulnerability_rule(code)
    )

    vulnerability = []

    detection_source = "AI_MODEL"

    # ==========================================
    # RULE ENGINE PRIORITY
    # ==========================================

    if rule_vulnerability:

        vulnerability.append({

            "label": rule_vulnerability,

            "confidence": 99.9
        })

        detection_source = (
            "RULE_ENGINE"
        )

        logger.info(
            f"Rule matched: {rule_vulnerability}"
        )

    # ==========================================
    # AI FALLBACK
    # ==========================================

    else:

        ai_prediction = (
            predict_vulnerability(code)
        )

        vulnerability = (
            ai_prediction["predictions"]
        )

        logger.info(
            f"AI predictions: {vulnerability}"
        )

    # ==========================================
    # PRIMARY VULNERABILITY
    # ==========================================

    primary_vulnerability = vulnerability[0][
        "label"
    ]

    primary_confidence = vulnerability[0][
        "confidence"
    ]

    # ==========================================
    # SAFE THRESHOLD
    # ==========================================

    if (
        primary_confidence <
        CONFIDENCE_THRESHOLD
    ):

        primary_vulnerability = "SAFE"

    # ==========================================
    # RISK
    # ==========================================

    risk = calculate_risk(
        primary_vulnerability,
        primary_confidence
    )

    # ==========================================
    # EXPLANATION
    # ==========================================

    explanation = (
        generate_explanation(
            primary_vulnerability
        )
    )

    # ==========================================
    # FIX
    # ==========================================

    fixed_code = generate_fix(
        primary_vulnerability,
        code
    )

    # ==========================================
    # MESSAGE
    # ==========================================

    if primary_vulnerability == "SAFE":

        message = (
            "No vulnerability detected"
        )

    else:

        message = (
            f"{primary_vulnerability} detected"
        )

    logger.info(
        "Analysis completed"
    )

    return build_response(

        language=language,

        vulnerability=primary_vulnerability,

        confidence=primary_confidence,

        risk=risk,

        explanation=explanation,

        fixed_code=fixed_code,

        message=message,

        detection_source=detection_source
    )