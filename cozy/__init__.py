import os

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
