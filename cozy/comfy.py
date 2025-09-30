import io
import json
import os
import urllib.parse
import urllib.request
import uuid
from io import BytesIO

import websocket

from cozy.workflow import Workflow

COMFY_SERVER = os.getenv("COMFY_SERVER", "localhost:8188")
USE_SSL = os.getenv("USE_SSL", "false").lower() in ("true", "1", "yes")

WS_SCHEME = "wss" if USE_SSL else "ws"
HTTP_SCHEME = "https" if USE_SSL else "http"


CLIENT_ID = str(uuid.uuid4())


def _queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode("utf-8")
    req = urllib.request.Request(f"{HTTP_SCHEME}://{COMFY_SERVER}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())


def _gen_image(ws, workflow):
    prompt_id = _queue_prompt(workflow)["prompt_id"]
    current_node = ""
    output_images = dict()

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)

            # We only care about "executing" messages (even though progress_state could do the same thing)
            if message["type"] != "executing":
                continue

            data = message["data"]

            # We only care about messages for our prompt
            if data["prompt_id"] != prompt_id:
                continue
            # We are done when node is None
            if data["node"] is None:
                break

            # Track the current node
            current_node = data["node"]

        # Store bytes from the websocket
        else:
            if current_node != "save_image_websocket_node":
                continue
            images_output = output_images.get(current_node, [])
            images_output.append(out[8:])
            output_images[current_node] = images_output

    return output_images


def generate_image(wf: Workflow) -> BytesIO:
    ws = websocket.create_connection(
        f"{WS_SCHEME}://{COMFY_SERVER}/ws?clientId={CLIENT_ID}"
    )
    ws.send(json.dumps(wf.workflow))
    images = _gen_image(ws, wf.workflow)
    ws.close()

    return io.BytesIO(images["save_image_websocket_node"][0])
