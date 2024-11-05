import logging
from datetime import datetime


def setup_logger():
    # Create a logger object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Define log format with function name and timestamp
    formatter = logging.Formatter(
        "%(asctime)s [%(funcName)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger


# Initialize the logger once in the module
logger = setup_logger()
