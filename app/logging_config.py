import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    """Set up logging for the Flask app."""
    log_file = app.config["LOG_FILE"]

    log_dir = os.path.dirname(log_file)

    # Ensure the directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create the log file if it doesn't exist
    if not os.path.exists(log_file):
        open(log_file, "w").close()

    log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    if not app.logger.handlers:
        app.logger.addHandler(log_handler)
        app.logger.setLevel(logging.INFO)

    app.logger.info("Logging initialized successfully.")

