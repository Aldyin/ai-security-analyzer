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
    num_classes=NUM_CLASSES
).to(device)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.eval()


def predict_language(code: str):

    ids = encode_code(code)[:MAX_LEN]

    if len(ids) < MAX_LEN:
        ids += [PAD_IDX] * (MAX_LEN - len(ids))

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
        }
    }