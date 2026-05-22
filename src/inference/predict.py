import torch
import torch.nn.functional as F

from src.infrastructure.models.transformer_lang import (
    TransformerClassifier
)

from src.infrastructure.tokenizers.hf_tokenizer import (
    load_tokenizer
)

from src.config.base import *


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

    encoded = tokenizer.encode(code)

    ids = encoded.ids[:MAX_LEN]

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
        )[0]

    result = {}

    for i, label in enumerate(LANGUAGE_CLASSES):

        result[label] = round(
            probs[i].item(),
            4
        )

    return result