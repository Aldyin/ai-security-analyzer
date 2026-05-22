# ==========================================
# LANGUAGE RULES
# ==========================================

LANGUAGE_RULES = {

    "Python": [
        "def ",
        "import ",
        "print(",
        "eval(",
        "exec("
    ],

    "JavaScript": [
        "console.log",
        "function ",
        "innerHTML",
        "=>"
    ],

    "C": [
        "#include",
        "printf(",
        "scanf("
    ],

    "Java": [
        "public class",
        "System.out.println",
        "public static void main"
    ]
}


# ==========================================
# VULNERABILITY RULES
# ==========================================

VULN_RULES = {

    "COMMAND_INJECTION": [
        "os.system(",
        "subprocess.run(",
        "subprocess.call(",
        "subprocess.Popen("
    ],

    "RCE": [
        "eval(",
        "exec("
    ],

    "SQLI": [
        "SELECT * FROM",
        "\" + user_input",
        "' + user_input"
    ],

    "XSS": [
        "innerHTML",
        "document.write("
    ],

    "PATH_TRAVERSAL": [
        "../",
        "open(user_input)",
        "open(path)"
    ]
}


# ==========================================
# LANGUAGE DETECTION
# ==========================================

def detect_language_rule(code):

    for lang, patterns in LANGUAGE_RULES.items():

        for p in patterns:

            if p in code:

                return lang

    return None


# ==========================================
# VULN DETECTION
# ==========================================

def detect_vulnerability_rule(code):

    for vuln, patterns in VULN_RULES.items():

        for p in patterns:

            if p in code:

                return vuln

    return None


# ==========================================
# RISK LEVELS
# ==========================================

RISK_MAP = {

    "SAFE": "LOW",

    "SQLI": "HIGH",

    "XSS": "MEDIUM",

    "RCE": "CRITICAL",

    "PATH_TRAVERSAL": "HIGH",

    "COMMAND_INJECTION": "CRITICAL"
}


# ==========================================
# RISK CALCULATION
# ==========================================

def calculate_risk(
    vulnerability: str,
    confidence: float
):

    if confidence < 50:
        return "LOW"

    return RISK_MAP.get(
        vulnerability,
        "UNKNOWN"
    )