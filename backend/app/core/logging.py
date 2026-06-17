"""Logging configuration."""

import logging
import logging.handlers
from pathlib import Path
from app.config import settings

# Create logs directory
logs_dir = Path(settings.LOG_FILE).parent
logs_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logger = logging.getLogger(settings.APP_NAME)
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

# File handler
file_handler = logging.handlers.RotatingFileHandler(
    settings.LOG_FILE,
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
)
logger.addHandler(console_handler)


def get_logger():
    """Get application logger."""
    return logger
