def build_response(

    language,
    vulnerability,
    confidence,
    risk,
    explanation,
    fixed_code,
    message,
    detection_source

):

    return {

        "language": language,

        "vulnerability": vulnerability,

        "confidence": confidence,

        "risk": risk,

        "explanation": explanation,

        "fixed_code": fixed_code,

        "message": message,

        "detection_source": detection_source
    }