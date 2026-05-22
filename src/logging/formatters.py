import logging


DEFAULT_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def build_formatter():

    return logging.Formatter(
        DEFAULT_FORMAT
    )