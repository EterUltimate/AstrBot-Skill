import os
from dotenv import load_dotenv

load_dotenv()

def _get_int_env(name: str, default: int) -> int:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
    GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
    BASE_URL = (os.getenv("BASE_URL") or os.getenv("OPENAI_API_BASE") or "https://generativelanguage.googleapis.com").strip()
    GEMINI_API_VERSION = os.getenv("GEMINI_API_VERSION", "v1beta").strip()
    MODEL_NAME = (os.getenv("MODEL_NAME") or "gemini-1.5-flash").strip()
    LLM_API_STYLE = os.getenv("LLM_API_STYLE", "auto").strip()
    SHOW_BASE_URL_IN_LOGS = os.getenv("SHOW_BASE_URL_IN_LOGS", "0").strip() == "1"
    LLM_MAX_TOKENS = _get_int_env("LLM_MAX_TOKENS", 12000)
    REPO_NAME = "AstrBotDevs/AstrBot"
    STATE_FILE = "scripts/state.json"

config = Config()
