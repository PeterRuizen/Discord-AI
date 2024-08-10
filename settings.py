import os
import logging
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)-10s - %(module)-15s - %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
        },
        "console2": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "level": "INFO",
            "mode": "w",
            "formatter": "verbose"
        }
    },
    "loggers": {
        "bot": {
            "level": "INFO",
            "handlers": ['console'],
            "propagate": False
        },
        "discord": {
            "level": "INFO",
            "handlers": ['console2', 'file'],
            "propagate": False
        },
    }
}

dictConfig(LOGGING_CONFIG)