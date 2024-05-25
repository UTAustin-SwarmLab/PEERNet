"""Exposes ch, a custom stream handler for printing with color.

Adapted from https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output.

Typical usage example:
    from custom_formatter import ch
    #Instantiate a logger however you like
    logger.add_handler(ch)
"""

import logging


class CustomFormatter(logging.Formatter):
    """Custom formatting handler to print logging with color in the terminal."""

    orange = "\x1b[38;5;208m"  # ANSI escape code for orange
    blue = "\x1b[38;5;27m"  # ANSI escape code for blue
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: orange + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        """Aplies format to incoming record. Shouldn't be required for a user to run."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
