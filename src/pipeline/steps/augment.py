import random
import pandas as pd
import os

from src.logging.logger import get_logger

logger = get_logger("pipeline.augment", "logs/pipeline.log")

AUG_REPEAT = 2


def augment():
    input_path = "data/language/train.csv"
    output_path = "data/language/train_augmented.csv"

    if not os.path.exists(input_path):
        logger.warning("train.csv not found")
        return

    df = pd.read_csv(input_path)

    data = []

    for _, row in df.iterrows():
        code = str(row["code"])
        label = row["label"]

        data.append((code, label))

        for _ in range(AUG_REPEAT):
            data.append((code.lower(), label))

    random.shuffle(data)

    pd.DataFrame(data, columns=["code", "label"]).to_csv(output_path, index=False)

    logger.info(f"Augmented: {len(data)} samples")