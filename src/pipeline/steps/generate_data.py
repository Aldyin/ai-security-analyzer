import subprocess
import sys
from src.logging.logger import get_logger

logger = get_logger("pipeline.generate", "logs/pipeline.log")


def generate():
    logger.info("Generating language dataset...")

    subprocess.run(
        [sys.executable, "prepare_lots_of_code.py"],
        check=True
    )

    logger.info("Language dataset generated")