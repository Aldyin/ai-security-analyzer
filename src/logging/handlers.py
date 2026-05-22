import logging

from pathlib import Path

from src.logging.formatters import build_formatter


LOG_DIR = Path("logs")

LOG_DIR.mkdir(
    exist_ok=True
)


def build_console_handler():

    handler = logging.StreamHandler()

    handler.setFormatter(
        build_formatter()
    )

    return handler


def build_file_handler(name: str):

    handler = logging.FileHandler(
        LOG_DIR / f"{name}.log"
    )

    handler.setFormatter(
        build_formatter()
    )

    return handler