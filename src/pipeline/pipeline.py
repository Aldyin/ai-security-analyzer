# src/pipeline/pipeline.py

from src.logging.logger import get_logger

from src.pipeline.steps.clean import clean
from src.pipeline.steps.generate_data import generate
from src.pipeline.steps.augment import augment

from src.pipeline.steps.train_lang import train_lang
from src.pipeline.steps.train_vuln import train_vuln


logger = get_logger("pipeline", "logs/pipeline.log")


def safe_step(name, fn, allow_fail=False):
    logger.info(f"▶ START: {name}")

    try:
        fn()
        logger.info(f"✔ DONE: {name}")
    except Exception as e:
        logger.exception(f"✖ FAILED: {name}")

        if not allow_fail:
            raise e


def run():
    logger.info("🚀 PIPELINE STARTED")

    try:
        safe_step("CLEAN", clean)
        safe_step("GENERATE", generate, allow_fail=True)
        safe_step("AUGMENT", augment)

        safe_step("TRAIN_LANG", train_lang)
        safe_step("TRAIN_VULN", train_vuln, allow_fail=True)

        logger.info("🔥 PIPELINE COMPLETED")

    except Exception:
        logger.exception("❌ PIPELINE FAILED")


if __name__ == "__main__":
    run()