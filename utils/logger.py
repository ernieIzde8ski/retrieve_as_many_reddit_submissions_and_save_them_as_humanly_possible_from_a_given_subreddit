import logging
from pathlib import Path


def get_level(level: int | str | None, default: int = logging.INFO) -> int:
    if isinstance(level, int):
        return level
    elif level is None:
        return default
    return getattr(logging, level or "", None) or default


def get_logger(path: str | Path, std_level: int | str | None, logger_name: str | None = None) -> logging.Logger:
    std_level = get_level(std_level)
    # For some reason, it has to be NOTSET in order for the logger to actually work
    logger = logging.getLogger(logger_name)
    logger.setLevel(0)

    # initialize loggers
    stdlog = logging.StreamHandler()
    stdlog.setLevel(std_level)

    file = logging.FileHandler(path)
    file.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(relativeCreated)d | %(levelname)s | %(message)s")
    stdlog.setFormatter(formatter)
    file.setFormatter(formatter)

    # add loggers to handler
    logger.handlers = [stdlog, file]
    logger.debug("Retrieved logger successfully")

    return logger
