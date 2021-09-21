import logging
import sys
import time
from contextlib import contextmanager

from loguru import logger


@contextmanager
def log(desc):
    logger.info(f"Function running: {desc}")
    start = time.time()
    try:
        yield
    except Exception as e:
        logger.exception(f"Error encountered on: {desc}", e)
        raise
    finally:
        duree = time.time() - start
        logger.info(f"Time spent on {desc}: {duree}s")


def configure_logger():
    """Configure the logger. The logs would be written to stdout, log.log and debug.log"""
    DEBUG = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"  # noqa: E501
    INFO = "<level>{message}</level>"

    handlers = [
        {"sink": sys.stderr, "level": "INFO", "format": INFO},
        {"sink": "log.log", "level": "INFO", "format": DEBUG},
        {"sink": "debug.log", "level": "DEBUG", "format": DEBUG},
    ]
    if "pytest" in sys.modules:
        # Only activate stderr in unittest
        handlers = handlers[:1]

    logger.configure(handlers=handlers)

    # Intercept standard logging messages toward your Loguru sinks
    # https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Ignore some over-verbose useless logs
        name = record.name.split(".")[0]
        if name in ("tensorboard"):
            return

        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
