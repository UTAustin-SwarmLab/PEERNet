"""Tests custom formatting"."""

from peernet.utils import ch
import logging

logger = logging.getLogger("test_custom_formatter")
logger.setLevel(logging.DEBUG)


def test_ch():
    """Ensures ch can be imported and applied to a logger."""
    logger.addHandler(ch)
    print("\n")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warn("This is a warning")
    logger.error("This is an error message")
    logger.critical("This is a critical error message")
