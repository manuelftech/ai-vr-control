from config.config_vars import config
import colorlog
import logging
import sys

def configure_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        colorlog.ColoredFormatter(
            config.LOGGER_FORMAT, 
            datefmt=config.LOGGER_DATE_FORMAT, 
            log_colors=config.LOGGER_COLOR_FORMAT)
    )
    logging.basicConfig(level=config.LOGGER_LEVEL, handlers=[handler])
