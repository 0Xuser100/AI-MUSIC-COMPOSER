"""Simple Loguru configuration for the AI Music Composer project."""

from pathlib import Path
import sys

from loguru import logger

LOG_FILE = Path(__file__).resolve().parent / "musicllm.log"


def setup_logger(level: str = "INFO"):
    """Configure Loguru to log to stdout and a local file."""

    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )
    logger.add(
        LOG_FILE,
        level=level,
        rotation="5 MB",
        retention="7 days",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )
    return logger


__all__ = ["setup_logger", "LOG_FILE"]
