import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    """Set up logging for the Flask app."""
    log_file = app.config["LOG_FILE"]

    if not os.path.exists(log_file):
        open(log_file, "w").close()

    log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)
