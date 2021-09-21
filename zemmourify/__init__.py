"""Top-level package for zemmourify."""

__version__ = "0.0.4"

from dotenv import find_dotenv, load_dotenv
from loguru import logger

from zemmourify.logs import configure_logger

# Load .env file
load_dotenv(find_dotenv())

# Configure loguru
configure_logger()

logger.info("App started")
