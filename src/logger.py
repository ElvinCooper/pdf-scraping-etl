# src/logger.py

import logging
import os


def setup_logger():
    """
    Configures logging for the project.
    Logs to both the console and a file (logs/app.log).
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )

    return logging.getLogger(__name__)


# Initialize the logger
logger = setup_logger()
