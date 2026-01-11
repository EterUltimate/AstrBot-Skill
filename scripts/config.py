import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
    GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
    BASE_URL = (os.getenv("BASE_URL") or os.getenv("OPENAI_API_BASE") or "https://generativelanguage.googleapis.com").strip()
    MODEL_NAME = (os.getenv("MODEL_NAME") or "gemini-1.5-flash").strip()
    REPO_NAME = "AstrBotDevs/AstrBot"
    STATE_FILE = "scripts/state.json"

config = Config()
