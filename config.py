import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SECRET_KEY   = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
