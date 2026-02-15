import os
import sys
from logging.config import dictConfig

try:
    from colorlog import ColoredFormatter
except ImportError:
    ColoredFormatter = None


def setup_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    log_format = "%(asctime)s [%(levelname)s] %(name)s %(message)s"

    if ColoredFormatter:
        formatter = {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s" + log_format,
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        }
    else:
        formatter = {"format": log_format}

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": formatter,
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "default",
                    "stream": sys.stdout,
                },
            },
            "loggers": {
                "app": {
                    "handlers": ["console"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["console"],
                    "level": log_level,
                    "propagate": False,
                },
                # accessログがうるさければ WARNING に
                "uvicorn.access": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": log_level,
            },
        }
    )
