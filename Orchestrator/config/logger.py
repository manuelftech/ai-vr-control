from config import config
import logging.config

def configure_logging():
    """
    Initializes the main logger
    """

    LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': config.LOGGER_FORMAT,
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'standard': {
            'format': "%(levelname)s: %(asctime)s - %(name)s:%(filename)s:%(lineno)d - %(message)s",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'ai-vr-control.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    }
    logging.config.dictConfig(LOGGING_CONFIG)