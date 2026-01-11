import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE") or os.getenv("BASE_URL") or "https://api.openai.com/v1"
    REPO_NAME = "AstrBotDevs/AstrBot"
    STATE_FILE = "scripts/state.json"

config = Config()
