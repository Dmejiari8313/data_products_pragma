"""Central logging configuration for the Movies EDA dashboard.

This module provides a single entry point to configure the standard library
``logging`` so every layer emits traceable, consistently formatted log records.
"""

from __future__ import annotations

import logging

DEFAULT_LOG_LEVEL: int = logging.INFO
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: int = DEFAULT_LOG_LEVEL) -> None:
    """Configure the root logger for the application.

    The configuration is idempotent: calling it multiple times does not add
    duplicate handlers to the root logger.

    Parameters
    ----------
    level : int, optional
        Logging level to apply to the root logger. Defaults to
        :data:`DEFAULT_LOG_LEVEL` (``logging.INFO``).

    Returns
    -------
    None
        This function configures logging as a side effect and returns nothing.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger with the given name.

    Parameters
    ----------
    name : str
        Name of the logger, typically ``__name__`` of the calling module.

    Returns
    -------
    logging.Logger
        A configured :class:`logging.Logger` instance.
    """
    return logging.getLogger(name)
