import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

COMFY_SERVER = os.getenv("COMFY_SERVER", "localhost:8188")
USE_SSL = os.getenv("USE_SSL", "false").lower() in ("true", "1", "yes")

WS_SCHEME = "wss" if USE_SSL else "ws"
HTTP_SCHEME = "https" if USE_SSL else "http"

NEGATIVE_PROMPT = os.getenv(
    "NEGATIVE_PROMPT",
    "nudity, violence, gore, blood, sexual content, explicit, offensive",
)

MAX_RESOLUTION = int(os.getenv("MAX_RESOLUTION", 1280))
MAX_STEPS = int(os.getenv("MAX_STEPS", 50))
WORKFLOW_PATH = Path(os.getenv("WORKFLOW_PATH", "workflows/flux1-dev-fp8.json"))
