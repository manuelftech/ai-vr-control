import logging
from config import config

def init_logging():
    """
    Initializes the main logger
    """
    logging.basicConfig(level=config.LOGGING_LEVEL, format=config.LOGGER_FORMAT)
    logging.info("Logger configured")