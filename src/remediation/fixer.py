def generate_fix(
    vulnerability: str,
    code: str
):

    if vulnerability == "SQLI":

        return code.replace(
            '"+ user_input +"',
            "?"
        )

    elif vulnerability == "XSS":

        return code.replace(
            "innerHTML",
            "textContent"
        )

    elif vulnerability == "RCE":

        return (
            "# Avoid eval/exec usage\n"
            + code
        )

    elif vulnerability == "PATH_TRAVERSAL":

        return (
            "# Validate file paths\n"
            + code
        )

    elif vulnerability == "COMMAND_INJECTION":

        return (
            "# Avoid shell command execution\n"
            + code
        )

    return code