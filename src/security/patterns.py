PATTERNS = {
    "RCE": [
        "eval(",
        "exec(",
        "os.system",
        "subprocess"
    ],
    "SQLI": [
        "select",
        "insert",
        "update",
        "delete"
    ],
    "XSS": [
        "<script>",
        "innerhtml",
        "document.write"
    ],
    "PATH_TRAVERSAL": [
        "../",
        "..\\"
    ],
    "COMMAND_INJECTION": [
        "system(",
        "popen("
    ]
}