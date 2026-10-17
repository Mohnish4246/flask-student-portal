
from dotenv import load_dotenv
import os

load_dotenv()

# Gets the absolute path of the folder containing config.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY") # sessions,flash messages,CSRF protection layer

    # OLD: Relative path (depends on where the terminal runs Flask)
    # UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER",'static/uploads')

    # NEW: Absolute path (works regardless of the terminal's current folder)
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        os.getenv("UPLOAD_FOLDER", "static/uploads")
    )

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH",2097152))

    DATABASE = os.getenv("DATABASE","students.db")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
