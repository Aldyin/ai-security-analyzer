import torch
import torch.nn.functional as F

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
    num_classes=len(VULN_CLASSES)
).to(DEVICE)


model.load_state_dict(
    torch.load(
        "artifacts/model_vuln.pth",
        map_location=DEVICE
    )
)

model.eval()


def predict_vulnerability(code: str):

    tokens = encode_code(code)

    x = torch.tensor(
        [tokens],
        dtype=torch.long
    ).to(DEVICE)

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

    vulnerability = VULN_CLASSES[
        pred.item()
    ]

    return {

        "label": vulnerability,

        "confidence": round(
            confidence.item() * 100,
            2
        ),

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