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
    calculate_risk,
    detect_language_rule,
    detect_vulnerability_rule
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
    # LANGUAGE DETECTION
    # ==========================================

    ai_language = predict_language(code)

    rule_language = detect_language_rule(code)

    if rule_language is not None:

        language = {

            "label": rule_language,

            "confidence": 99.9,

            "source": "RULE_ENGINE",

            "probabilities": {
                rule_language: 99.9
            }
        }

    else:

        language = {

            **ai_language,

            "source": "AI_MODEL"
        }

    logger.info(
        f"Detected language: {language}"
    )

    # ==========================================
    # VULNERABILITY DETECTION
    # ==========================================

    ai_vuln = predict_vulnerability(code)

    rule_vuln = detect_vulnerability_rule(code)

    if rule_vuln is not None:

        vulnerability = rule_vuln

        confidence = 99.9

        detection_source = "RULE_ENGINE"

    else:

        vulnerability = ai_vuln["label"]

        confidence = ai_vuln["confidence"]

        detection_source = "AI_MODEL"

    logger.info(
        f"Detected vulnerability: {vulnerability}"
    )

    # ==========================================
    # RISK ANALYSIS
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
    # AUTO FIX
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

        confidence=confidence,

        risk=risk,

        explanation=explanation,

        fixed_code=fixed_code,

        message=message,

        detection_source=detection_source
    )