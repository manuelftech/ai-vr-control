import logging
from config import config

def init_logging():
    """
    Initializes the main logger
    """
    logging.basicConfig(level=logging.DEBUG, format=config.LOGGER_FORMAT)
    logging.info("Logger configured")