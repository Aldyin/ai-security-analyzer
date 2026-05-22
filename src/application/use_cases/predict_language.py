import torch
import torch.nn.functional as F

from src.infrastructure.models.transformer_lang import (
    TransformerClassifier
)

from src.infrastructure.tokenizers.hf_tokenizer import (
    load_tokenizer,
    encode_code
)

from src.config import *


MODEL_PATH = "artifacts/model_lang.pth"

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

tokenizer = load_tokenizer()

model = TransformerClassifier(
    vocab_size=30000,
    embed_dim=EMBED_DIM,
    num_heads=NUM_HEADS,
    ff_dim=FF_DIM,
    num_layers=NUM_LAYERS,
    num_classes=len(LANGUAGE_CLASSES)
).to(device)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.eval()


# ==========================================
# RULE-BASED DETECTION
# ==========================================

def detect_language_rules(code: str):

    code_lower = code.lower()

    # Python
    if (
        ("import" in code_lower and "input(" in code_lower)
        or "def " in code_lower
        or "self" in code_lower
        or "print(" in code_lower
    ):
        return "Python"

    # Java
    if (
        "public class" in code_lower
        or "system.out.println" in code_lower
    ):
        return "Java"

    # JavaScript
    if (
        "console.log" in code_lower
        or "=>" in code_lower
        or "function(" in code_lower
    ):
        return "JavaScript"

    # C
    if (
        "#include" in code_lower
        or "printf(" in code_lower
    ):
        return "C"

    return None


# ==========================================
# HYBRID LANGUAGE PREDICTION
# ==========================================

def predict_language(code: str):

    # ==========================================
    # RULE ENGINE
    # ==========================================

    rule_lang = detect_language_rules(
        code
    )

    print(
        "RULE LANGUAGE:",
        rule_lang
    )

    if rule_lang:

        return {

            "label": rule_lang,

            "confidence": 99.9,

            "probabilities": {

                lang: (
                    99.9
                    if lang == rule_lang
                    else 0.1
                )

                for lang in LANGUAGE_CLASSES
            },

            "source": "RULE_ENGINE"
        }

    # ==========================================
    # AI FALLBACK
    # ==========================================

    ids = encode_code(code)[:MAX_LEN]

    if len(ids) < MAX_LEN:

        ids += [PAD_IDX] * (
            MAX_LEN - len(ids)
        )

    x = torch.tensor(
        [ids],
        dtype=torch.long
    ).to(device)

    with torch.no_grad():

        logits = model(x)

        probs = F.softmax(
            logits,
            dim=1
        )

        confidence, pred = torch.max(
            probs,
            dim=1
        )

    language = LANGUAGE_CLASSES[
        pred.item()
    ]

    return {

        "label": language,

        "confidence": round(
            confidence.item() * 100,
            2
        ),

        "probabilities": {

            LANGUAGE_CLASSES[i]: round(
                probs[0][i].item() * 100,
                2
            )

            for i in range(
                len(LANGUAGE_CLASSES)
            )
        },

        "source": "AI_MODEL"
    }