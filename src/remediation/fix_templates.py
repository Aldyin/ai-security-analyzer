FIX_TEMPLATES = {

    "RCE": {
        "risk": "CRITICAL",

        "explanation":
            "Using eval/exec on untrusted input may execute arbitrary code.",

        "fixes": {
            "Python": {
                "bad": "eval(user_input)",

                "good":
'''import ast

safe_data = ast.literal_eval(user_input)
'''
            }
        }
    },

    "COMMAND_INJECTION": {
        "risk": "CRITICAL",

        "explanation":
            "Shell commands built from user input may allow command injection.",

        "fixes": {
            "Python": {
                "bad": "os.system(user_input)",

                "good":
'''import subprocess

subprocess.run(
    [\"ls\", \"-la\"],
    check=True
)
'''
            }
        }
    },

    "SQL_INJECTION": {
        "risk": "HIGH",

        "explanation":
            "Dynamic SQL queries may allow attackers to manipulate queries.",

        "fixes": {
            "Python": {
                "bad":
'''query = "SELECT * FROM users WHERE id = " + user_id''',

                "good":
'''cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (user_id,)
)
'''
            }
        }
    },

    "PATH_TRAVERSAL": {
        "risk": "HIGH",

        "explanation":
            "User-controlled file paths may access unintended files.",

        "fixes": {
            "Python": {
                "bad":
'''open(user_path)''',

                "good":
'''from pathlib import Path

base = Path("/safe/root")

safe_path = (base / user_path).resolve()

if not str(safe_path).startswith(str(base)):
    raise ValueError("Invalid path")
'''
            }
        }
    },

    "XSS": {
        "risk": "MEDIUM",

        "explanation":
            "Unsanitized HTML output may execute JavaScript in browsers.",

        "fixes": {
            "JavaScript": {
                "bad":
'''element.innerHTML = user_input''',

                "good":
'''element.textContent = user_input'''
            }
        }
    }
}