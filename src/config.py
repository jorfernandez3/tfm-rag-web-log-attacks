import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")
MODEL_NAME = os.getenv("OPEN_MODEL", "gpt-4o-mini")