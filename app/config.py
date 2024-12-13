import os

class Config:
    BASE_DIR = os.path.abspath(os.getcwd())  # Base directory
    TABLE_NAME = "harmonized_data"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    SCHEMA_FILE = os.path.join(BASE_DIR, "etl_info", "schema.json")
    API_KEY_FILE = os.path.join(BASE_DIR, "etl_info", "api_key.txt")
    LOG_FILE = os.path.join(BASE_DIR, "etl_info", "app_log.log")

    @staticmethod
    def init_app(app):
        pass
