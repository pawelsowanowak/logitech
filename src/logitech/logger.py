import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logger(logger_name: str) -> logging.Logger:
    """Configure and return a logger with file handling and formatting.

    Creates a logger that writes to a rotating log file with a specific format.
    The log file is created in the 'logs' directory relative to this module's location.

    :param logger_name: Name for the logger instance
    :type logger_name: str
    :returns: Configured logger instance
    :rtype: logging.Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    log_dir = Path(__file__).parents[2] / "logs" / "automation"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{logger_name}.log"

    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=5  # 1MB
    )
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
