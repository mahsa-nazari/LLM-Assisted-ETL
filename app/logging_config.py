import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import pytz

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, timezone=None):
        super().__init__(fmt, datefmt)
        self.timezone = timezone

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=self.timezone)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%d %H:%M:%S")  # Default readable format

def configure_logging(app):
    log_file = app.config["LOG_FILE"]
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(log_file):
        open(log_file, "w").close()

    log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
    log_handler.setLevel(logging.INFO)
    timezone = pytz.timezone("Europe/Brussels")  # Set Brussels timezone
    formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s', timezone=timezone)
    log_handler.setFormatter(formatter)

    if not app.logger.handlers:
        app.logger.addHandler(log_handler)
        app.logger.setLevel(logging.INFO)

    app.logger.info("Logging initialized successfully.")
