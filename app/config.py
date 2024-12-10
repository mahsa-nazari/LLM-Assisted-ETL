import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.getcwd()), "uploads")
    SCHEMA_FILE = os.path.join(os.path.abspath(os.getcwd()), "schema.json")
    TABLE_NAME = "harmonized_data"
    API_KEY_FILE = os.path.join(os.path.abspath(os.getcwd()), "apy_key.txt")
    LOG_FILE = os.path.join(os.path.abspath(os.getcwd()), "app.log")

    @staticmethod
    def init_app(app):
        pass
