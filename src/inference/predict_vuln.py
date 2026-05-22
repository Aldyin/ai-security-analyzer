import torch

from src.config import *

from src.infrastructure.models.transformer_vuln import (
    VulnerabilityClassifier
)

from src.infrastructure.tokenizers.hf_tokenizer import (
    encode_code
)


model = VulnerabilityClassifier(

    vocab_size=30000,

    embed_dim=EMBED_DIM,

    num_heads=NUM_HEADS,

    ff_dim=FF_DIM,

    num_layers=NUM_LAYERS,

    num_classes=VULN_NUM_CLASSES

).to(DEVICE)


model.load_state_dict(

    torch.load(

        "artifacts/model_vuln.pth",

        map_location=DEVICE
    )
)

model.eval()


def predict_vulnerability(code: str):

    tokens = encode_code(
        code
    )[:MAX_LEN]

    if len(tokens) < MAX_LEN:

        tokens += [PAD_IDX] * (
            MAX_LEN - len(tokens)
        )

    x = torch.tensor(

        [tokens],

        dtype=torch.long

    ).to(DEVICE)

    with torch.no_grad():

        logits = model(x)

        # ======================================
        # MULTI-LABEL PROBABILITIES
        # ======================================

        probs = torch.sigmoid(
            logits
        )

    predictions = []

    # ======================================
    # THRESHOLD DETECTION
    # ======================================

    for i, prob in enumerate(
        probs[0]
    ):

        score = round(
            prob.item() * 100,
            2
        )

        # ======================================
        # CALIBRATED THRESHOLD
        # ======================================

        if score >= 45:

            predictions.append({

                "label": VULN_CLASSES[i],

                "confidence": score
            })

    # ======================================
    # SAFE FALLBACK
    # ======================================

    if not predictions:

        predictions.append({

            "label": "SAFE",

            "confidence": 100.0
        })

    return {

        "predictions": predictions,

        "probabilities": {

            VULN_CLASSES[i]: round(
                probs[0][i].item() * 100,
                2
            )

            for i in range(
                len(VULN_CLASSES)
            )
        }
    }