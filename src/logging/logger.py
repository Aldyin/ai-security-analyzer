import logging

from pathlib import Path


LOG_DIR = Path("logs")

LOG_DIR.mkdir(
    exist_ok=True
)


def get_logger(
    name: str,
    log_file: str | None = None
):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # ==========================================
    # CONSOLE HANDLER
    # ==========================================

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    # ==========================================
    # FILE HANDLER
    # ==========================================

    if log_file is None:

        log_path = LOG_DIR / f"{name}.log"

    else:

        log_path = Path(log_file)

        if not log_path.is_absolute():

            if not str(log_path).startswith("logs/"):

                log_path = LOG_DIR / log_path

    log_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file_handler = logging.FileHandler(
        log_path
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    return logger
