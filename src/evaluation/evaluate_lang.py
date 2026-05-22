from sklearn.metrics import (
    classification_report
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

        y_pred.append(pred)

    report = classification_report(
        y_true,
        y_pred
    )

    print(report)

    return report