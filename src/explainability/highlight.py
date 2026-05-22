import re


DANGEROUS_PATTERNS = {

    "RCE": [
        r"\beval\s*\(",
        r"\bexec\s*\("
    ],

    "COMMAND_INJECTION": [
        r"\bos\.system\s*\(",
        r"\bsubprocess\."
    ],

    "SQL_INJECTION": [
        r"SELECT.+\+",
        r"INSERT.+\+",
        r"DELETE.+\+"
    ],

    "PATH_TRAVERSAL": [
        r"\.\./",
        r"open\s*\("
    ],

    "XSS": [
        r"innerHTML",
        r"document\.write"
    ]
}


def highlight_vulnerabilities(code: str):

    findings = []

    for vuln, patterns in DANGEROUS_PATTERNS.items():

        for pattern in patterns:

            matches = re.finditer(
                pattern,
                code,
                re.IGNORECASE
            )

            for match in matches:

                findings.append({

                    "vulnerability": vuln,

                    "match": match.group(),

                    "start": match.start(),

                    "end": match.end()
                })

    return findings


if __name__ == "__main__":

    sample = """
eval(user_input)

os.system(cmd)

query = "SELECT * FROM users WHERE id=" + user_id
"""

    results = highlight_vulnerabilities(sample)

    for r in results:
        print(r)