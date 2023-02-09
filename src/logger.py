import logging

LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}
gunicorn_logger = logging.getLogger("gunicorn.error")


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Get a logger.
    Args:
        name (str): The name of the logger.
        level (int, optional): The level of the logger. Defaults to logging.DEBUG.
    Returns:
        logging.Logger: The logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger.handlers = gunicorn_logger.handlers
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
