import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score


def classification_metrics(y_true, y_pred):
    return {
        "precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


def multilabel_metrics(y_true, y_pred, threshold=0.5):
    y_pred_bin = (y_pred > threshold).astype(int)

    return {
        "precision": precision_score(y_true, y_pred_bin, average="micro", zero_division=0),
        "recall": recall_score(y_true, y_pred_bin, average="micro", zero_division=0),
        "f1": f1_score(y_true, y_pred_bin, average="micro", zero_division=0),
    }