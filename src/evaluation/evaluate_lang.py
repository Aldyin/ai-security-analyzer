from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from src.inference.predict import (
    predict_language
)


def evaluate(samples):

    y_true = []

    y_pred = []

    for code, label in samples:

        pred = predict_language(code)

        y_true.append(label)

        y_pred.append(
            pred["label"]
        )

    print("\n===== LANGUAGE EVALUATION =====")

    print(
        f"Accuracy : "
        f"{accuracy_score(y_true, y_pred):.4f}"
    )

    print(
        f"Precision: "
        f"{precision_score(y_true, y_pred, average='weighted'):.4f}"
    )

    print(
        f"Recall   : "
        f"{recall_score(y_true, y_pred, average='weighted'):.4f}"
    )

    print(
        f"F1 Score : "
        f"{f1_score(y_true, y_pred, average='weighted'):.4f}"
    )

    print("\n===== CLASSIFICATION REPORT =====")

    print(
        classification_report(
            y_true,
            y_pred
        )
    )