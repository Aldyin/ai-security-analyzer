from src.inference.predict import predict_language
from src.inference.predict_vuln import predict_vulnerability

from src.security.rules import detect_vulnerability_rule
from src.security.rules import detect_language_rule

from src.remediation.fixer import generate_fix

from src.remediation.explanations import (
    get_explanation
)


# ==========================================
# RISK
# ==========================================

def calculate_risk(confidence):

    if confidence >= 80:
        return "CRITICAL"

    if confidence >= 60:
        return "HIGH"

    if confidence >= 40:
        return "MEDIUM"

    return "LOW"


# ==========================================
# TOP PREDICTION
# ==========================================

def get_top_prediction(results):

    label = max(
        results,
        key=results.get
    )

    confidence = round(
        results[label] * 100,
        2
    )

    return label, confidence


# ==========================================
# MAIN
# ==========================================

def auto_analyze(code):

    # ======================================
    # LANGUAGE
    # ======================================

    rule_lang = detect_language_rule(code)

    if rule_lang:

        language = rule_lang
        lang_conf = 99.0

    else:

        lang_results = predict_language(code)

        language, lang_conf = get_top_prediction(
            lang_results
        )

    # ======================================
    # VULNERABILITY
    # ======================================

    rule_vuln = detect_vulnerability_rule(code)

    if rule_vuln:

        vuln = rule_vuln
        confidence = 99.0

    else:

        vuln_results = predict_vulnerability(
            code
        )

        vuln, confidence = get_top_prediction(
            vuln_results
        )

    # ======================================
    # RISK
    # ======================================

    risk = calculate_risk(confidence)

    # ======================================
    # FIX
    # ======================================

    fixed_code = generate_fix(
        vuln,
        language,
        code
    )

    # ======================================
    # EXPLANATION
    # ======================================

    explanation = get_explanation(
        vuln
    )

    # ======================================
    # MESSAGE
    # ======================================

    if vuln == "SAFE":

        message = "No vulnerabilities detected."

    else:

        message = (
            "Potential vulnerability detected."
        )

    # ======================================
    # RESULT
    # ======================================

    return {

        "language": language,

        "vulnerability": vuln,

        "confidence": confidence,

        "risk": risk,

        "explanation": explanation,

        "fixed_code": fixed_code,

        "message": message
    }