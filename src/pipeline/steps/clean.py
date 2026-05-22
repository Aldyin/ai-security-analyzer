import os
from src.utils.logger import get_logger

logger = get_logger("pipeline.clean", "logs/pipeline.log")

FILES = [
    "artifacts/model_vuln.pth",
    "data/train_augmented.csv",
]


def clean():
    logger.info("Cleaning...")

    for f in FILES:
        if os.path.exists(f):
            os.remove(f)
            logger.info(f"Removed: {f}")