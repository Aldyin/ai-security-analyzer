import torch

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    classification_report
)

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

    "cuda"

    if torch.cuda.is_available()

    else "cpu"
)


def evaluate():

    tokenizer = load_tokenizer()

    label_map = {

        v: i

        for i, v in enumerate(
            VULN_CLASSES
        )
    }

    dataset = VulnerabilityDataset(

        "data/vulnerability/test.csv",

        tokenizer,

        label_map
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

        num_classes=len(
            VULN_CLASSES
        )

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

            probs = torch.sigmoid(
                logits
            )

            # ======================================
            # CALIBRATED MULTI-LABEL THRESHOLD
            # ======================================

            preds = (
                probs >= 0.45
            ).float()

            y_true.extend(
                y.numpy()
            )

            y_pred.extend(
                preds.cpu().numpy()
            )

    # ======================================
    # METRICS
    # ======================================

    acc = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(

        y_true,

        y_pred,

        average="micro",

        zero_division=0
    )

    recall = recall_score(

        y_true,

        y_pred,

        average="micro",

        zero_division=0
    )

    f1 = f1_score(

        y_true,

        y_pred,

        average="micro",

        zero_division=0
    )

    # ======================================
    # OUTPUT
    # ======================================

    print(
        "\n===== VULNERABILITY EVALUATION ====="
    )

    print(f"Accuracy : {acc:.4f}")

    print(f"Precision: {precision:.4f}")

    print(f"Recall   : {recall:.4f}")

    print(f"F1 Score : {f1:.4f}")

    print(
        "\n===== CLASSIFICATION REPORT ====="
    )

    print(

        classification_report(

            y_true,

            y_pred,

            target_names=VULN_CLASSES,

            zero_division=0
        )
    )

    # ======================================
    # LABEL DISTRIBUTION
    # ======================================

    print(
        "\n===== LABEL DISTRIBUTION ====="
    )

    for i, vuln in enumerate(
        VULN_CLASSES
    ):

        true_count = sum(
            row[i] for row in y_true
        )

        pred_count = sum(
            row[i] for row in y_pred
        )

        print(

            f"{vuln}: "

            f"true={int(true_count)} | "

            f"predicted={int(pred_count)}"
        )


if __name__ == "__main__":

    evaluate()