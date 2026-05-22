import torch
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from torch.utils.data import DataLoader

from src.config import *

from src.infrastructure.datasets.vulnerability_dataset import (
    VulnerabilityDataset
)

from src.infrastructure.models.transformer_vuln import (
    VulnerabilityClassifier
)

from src.infrastructure.tokenizers.hf_tokenizer import (
    load_tokenizer
)


MODEL_PATH = "artifacts/model_vuln.pth"

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


def build_confusion_matrix():

    tokenizer = load_tokenizer()

    dataset = VulnerabilityDataset(
        "data/vulnerability/test.csv",
        tokenizer
    )

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE
    )

    model = VulnerabilityClassifier(
        vocab_size=30000,
        embed_dim=EMBED_DIM,
        num_heads=NUM_HEADS,
        ff_dim=FF_DIM,
        num_layers=NUM_LAYERS,
        num_classes=len(VULN_CLASSES)
    ).to(device)

    model.load_state_dict(
        torch.load(
            MODEL_PATH,
            map_location=device
        )
    )

    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():

        for x, y in loader:

            x = x.to(device)

            logits = model(x)

            preds = torch.argmax(
                logits,
                dim=1
            )

            y_true.extend(y.numpy())

            y_pred.extend(
                preds.cpu().numpy()
            )

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=VULN_CLASSES
    )

    fig, ax = plt.subplots(
        figsize=(10, 10)
    )

    disp.plot(
        ax=ax,
        cmap="Blues",
        xticks_rotation=45
    )

    plt.title(
        "Vulnerability Confusion Matrix"
    )

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    build_confusion_matrix()