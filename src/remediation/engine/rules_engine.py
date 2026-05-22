from src.remediation.fix_templates import (
    FIX_TEMPLATES
)


def get_fix_template(
    vulnerability: str
):

    return FIX_TEMPLATES.get(
        vulnerability,
        None
    )


def has_fix(
    vulnerability: str
):

    return vulnerability in FIX_TEMPLATES