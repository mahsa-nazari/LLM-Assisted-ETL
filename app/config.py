import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE_URI = os.getenv("DATABASE_URI")

