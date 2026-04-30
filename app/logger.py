from __future__ import annotations

import logging
from logging.config import dictConfig

from app.config import Config, get_settings


class ExtraFieldsFormatter(logging.Formatter):
    """Formatter that injects default values for optional extra fields."""

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "method"):
            record.method = "-"
        if not hasattr(record, "path"):
            record.path = "-"
        if not hasattr(record, "status_code"):
            record.status_code = "-"
        return super().format(record)


def configure_logging(settings: Config | None = None) -> None:
    settings = settings or get_settings()
    level = "DEBUG" if settings.is_dev() else "INFO"

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "app.logger.ExtraFieldsFormatter",
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(method)s %(path)s | status=%(status_code)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": level,
                },
            },
            "root": {
                "level": level,
                "handlers": ["console"],
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
            },
        }
    )
