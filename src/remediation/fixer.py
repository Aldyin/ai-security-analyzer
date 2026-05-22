# ==========================================
# FIX TEMPLATES
# ==========================================

FIXES = {

    # ======================================
    # RCE
    # ======================================

    ("RCE", "Python"):

'''
# Dangerous:
# eval(user_input)

# Safe alternative:

import ast

safe_input = ast.literal_eval(user_input)
''',

    # ======================================
    # COMMAND INJECTION
    # ======================================

    ("COMMAND_INJECTION", "Python"):

'''
# Dangerous:
# os.system(user_input)

# Safe alternative:

import subprocess

subprocess.run(
    ["ls", "-la"],
    check=True
)
''',

    # ======================================
    # SQLI
    # ======================================

    ("SQLI", "Python"):

'''
# Dangerous:
# query = "SELECT * FROM users WHERE id=" + user_id

# Safe alternative:

cursor.execute(
    "SELECT * FROM users WHERE id=%s",
    (user_id,)
)
''',

    # ======================================
    # XSS
    # ======================================

    ("XSS", "JavaScript"):

'''
// Dangerous:
// element.innerHTML = user_input

// Safe alternative:

element.textContent = user_input;
''',

    # ======================================
    # PATH TRAVERSAL
    # ======================================

    ("PATH_TRAVERSAL", "Python"):

'''
# Dangerous:
# open(user_input)

# Safe alternative:

import os

base = "/safe_directory"

path = os.path.abspath(
    os.path.join(base, user_input)
)

if path.startswith(base):
    open(path)
'''
}


# ==========================================
# MAIN API
# ==========================================

def generate_fix(vulnerability, language, code):

    key = (
        vulnerability,
        language
    )

    if key in FIXES:

        return FIXES[key]

    return (
        "No language-specific fix available."
    )