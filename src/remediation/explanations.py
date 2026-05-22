EXPLANATIONS = {

    "SAFE":
        "No vulnerabilities detected.",

    "SQLI":
        "SQL Injection allows attackers to manipulate database queries.",

    "XSS":
        "Cross-Site Scripting allows attackers to inject malicious JavaScript.",

    "RCE":
        "Remote Code Execution allows attackers to execute arbitrary code.",

    "PATH_TRAVERSAL":
        "Path Traversal allows attackers to access restricted filesystem paths.",

    "COMMAND_INJECTION":
        "Command Injection allows attackers to execute system commands."
}


def generate_explanation(vulnerability: str):

    return EXPLANATIONS.get(
        vulnerability,
        "Unknown vulnerability."
    )