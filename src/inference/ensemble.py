import torch

from src.inference.predict import predict_code
from src.inference.predict_vuln import predict_vulnerabilities

from src.infrastructure.tokenizers.hf_tokenizer import load_tokenizer
from src.infrastructure.models.transformer_lang import TransformerClassifier
from src.infrastructure.models.transformer_vuln import VulnerabilityClassifier


VULN_CLASSES = [
    "SQLI",
    "XSS",
    "RCE",
    "PATH_TRAVERSAL",
    "COMMAND_INJECTION",
    "SAFE"
]


def run():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = load_tokenizer()

    # --- language model ---
    lang_model = TransformerClassifier().to(device)
    lang_model.load_state_dict(torch.load("artifacts/model.pth", map_location=device))
    lang_model.eval()

    # --- vulnerability model ---
    vuln_model = VulnerabilityClassifier(len(VULN_CLASSES)).to(device)

    try:
        vuln_model.load_state_dict(
            torch.load("artifacts/model_vuln.pth", map_location=device)
        )
        vuln_model.eval()
        vuln_ready = True
    except:
        vuln_ready = False

    test_samples = [
        "print(5)",
        "eval(user_input)",
        "SELECT * FROM users WHERE id=" + "user_input",
        "<script>alert(1)</script>"
    ]

    print("\n=== ENSEMBLE RESULTS ===\n")

    for code in test_samples:
        print(f"Code: {code}")

        # language
        lang = predict_code(code, lang_model, tokenizer, device)
        print("Language:", lang)

        # vulnerabilities
        if vuln_ready:
            vulns = predict_vulnerabilities(code, vuln_model, tokenizer, device)
            print("Vulnerabilities:", vulns)
        else:
            print("Vulnerabilities: model not trained")

        print("-" * 50)


if __name__ == "__main__":
    run()