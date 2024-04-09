import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger():
    log_dir_path = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)
    log_file_path = os.path.join(log_dir_path, "app.log")

    # Create logger
    logger = logging.getLogger("app_logger")

    # Set up file handler with rotating logs
    file_handler = RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=10)

    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]"
        )
    )

    # Log Levels
    log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()  # Default to DEBUG if not specified
    file_handler.setLevel(getattr(logging, log_level))
    logger.addHandler(file_handler)
    logger.setLevel(getattr(logging, log_level))

    return logger


root_logger = setup_logger()
