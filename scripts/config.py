import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    BASE_URL = os.getenv("BASE_URL") or "https://generativelanguage.googleapis.com"
    MODEL_NAME = os.getenv("MODEL_NAME") or "gemini-1.5-flash"
    REPO_NAME = "AstrBotDevs/AstrBot"
    STATE_FILE = "scripts/state.json"

config = Config()
